from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import get_temperature
from settings import settings
from machine import Machine, PLC
import asyncio
import logging
from history import init_db, query_history
import time
from history import prune_older_than
from settings import settings
from pydantic import BaseModel


app = FastAPI(title="Machine Control Panel API")
# Allow requests from frontend
origins = [
    "http://localhost:5173",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],        # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# -----------------------------
# Data Models
# -----------------------------
class MotorRequest(BaseModel):
    speed: int

class ValveRequest(BaseModel):
    open: bool


# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,  # minimum level you want to capture
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# -----------------------------
# Machine State and PLC objects
# -----------------------------
machine = Machine()
plc = PLC(machine)

# -------------------------
# PLC scan loop
# -------------------------
@app.on_event("startup")
async def startup_event():
    # initialize telemetry DB
    await init_db()
    asyncio.create_task(plc.run())
    # start retention prune loop
    async def _prune_loop():
        while True:
            try:
                cutoff = int(time.time() * 1000) - settings.TELEMETRY_RETENTION_MS
                await prune_older_than(cutoff)
            except Exception:
                logger.exception("Error in telemetry prune loop")
            await asyncio.sleep(settings.TELEMETRY_PRUNE_INTERVAL)

    asyncio.create_task(_prune_loop())


# -----------------------------
# Endpoints
# -----------------------------

# Motor
@app.get("/motor")
def get_motor():
    snap = machine.snapshot()
    return {
        "speed": snap["motor_actual_speed"],
        "target": snap["motor_target_speed"],
        "min": settings.MIN_MOTOR_SPEED,
        "max": settings.MAX_MOTOR_SPEED,
    }

@app.post("/motor")
def set_motor(req: MotorRequest):
    requested_speed = req.speed
    logger.info(f"Request to change motor speed to: {requested_speed}")
    # Validate integer-ness
    try:
        if not float(requested_speed).is_integer():
            raise HTTPException(status_code=400, detail="Speed must be an integer.")
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Speed must be an integer.")

    # Clamp to backend-approved range
    clamped = max(settings.MIN_MOTOR_SPEED, min(settings.MAX_MOTOR_SPEED, int(requested_speed)))
    machine.set_motor_target(clamped)
    return {"speed": machine.snapshot()["motor_target_speed"]}


# Valve
@app.get("/valve")
def get_valve():
    return {"open": machine.snapshot()["valve_open"]}

@app.post("/valve")
def set_valve(req: ValveRequest):
    logger.info(f"Request to change valve state: {'Open' if req.open else 'Closed'}")
    machine.set_valve_target(req.open)
    return {"open": machine.snapshot()["valve_target"]}


# Temperature
@app.get("/temperature")
async def get_temp():
    logger.info(f"Requesting temperature value")
    data = await get_temperature()
    # data is {"temperature": val|None, "timestamp": iso_str|None}
    return data


# History
@app.get("/history")
async def get_history(start: int = None, end: int = None, limit: int = 1000):
    """Return telemetry samples. `start` and `end` are unix ms timestamps."""
    # validate params
    if limit > 10000:
        limit = 10000
    rows = await query_history(start, end, limit)
    # query_history returns chronological rows when a time window is provided,
    # and most-recent-first when no window was specified. In either case return
    # rows as-is (chronological for windowed requests).
    return rows


class ConfigResponse(BaseModel):
    telemetry_window_ms: int


@app.get("/config", response_model=ConfigResponse)
def get_config():
    """Return a small runtime configuration useful to the frontend."""
    return ConfigResponse(telemetry_window_ms=settings.TELEMETRY_WINDOW_MS)