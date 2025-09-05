from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import get_temperature
import asyncio

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
MIN_MOTOR_SPEED = 0
MAX_MOTOR_SPEED = 100
class MotorRequest(BaseModel):
    speed: int

class ValveRequest(BaseModel):
    open: bool

# -----------------------------
# Machine State (in-memory simulation)
# -----------------------------
machine_state = {
    "motor_actual_speed": 0,        # current motor speed
    "motor_target_speed": 0,        # target speed requested via POST
    "valve_open": False,            # current valve state
    "valve_target": False,          # target requested via POST
}

# -------------------------
# PLC scan loop
# -------------------------
SCAN_INTERVAL = 0.1  # seconds
VALVE_DELAY = 2    # seconds


async def plc_scan_loop():
    while True:
        # Motor: simulate gradual change in speed
        current_speed = machine_state["motor_actual_speed"]
        requested_speed = machine_state["motor_target_speed"]
        if requested_speed < current_speed:
            machine_state["motor_actual_speed"] -= 1
        elif requested_speed > current_speed:
            machine_state["motor_actual_speed"] += 1

        # Valve: simulate requested state with delay
        if machine_state["valve_open"] != machine_state["valve_target"]:
            machine_state["valve_open"] = machine_state["valve_target"]
            await asyncio.sleep(VALVE_DELAY)  # emulate physical actuation

        await asyncio.sleep(SCAN_INTERVAL)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(plc_scan_loop())


# -----------------------------
# Endpoints
# -----------------------------

# Motor
@app.get("/motor")
def get_motor():
    return {"speed": machine_state["motor_actual_speed"]}


@app.post("/motor")
def set_motor(req: MotorRequest):
    # enforce range of speeds
    requested_speed = req.speed
    machine_state["motor_target_speed"] = max(MIN_MOTOR_SPEED, min(MAX_MOTOR_SPEED, requested_speed))
    return {"speed": machine_state["motor_target_speed"]}


# Valve
@app.get("/valve")
def get_valve():
    return {"open": machine_state["valve_open"]}

@app.post("/valve")
def set_valve(req: ValveRequest):
    machine_state["valve_target"] = req.open
    return {"open": machine_state["valve_target"]}


# Temperature
@app.get("/temperature")
def get_temp():
    temperature = get_temperature()
    return {"temperature": temperature}