from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import get_temperature
from machine import Machine
import logging

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
# Machine State (in-memory simulation)
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,  # minimum level you want to capture
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# -----------------------------
# Machine State (in-memory simulation)
# -----------------------------
machine = Machine()

# -----------------------------
# Endpoints
# -----------------------------

# Motor
@app.get("/motor")
def get_motor():
    return {"speed": machine.snapshot()["motor_speed"]}

@app.post("/motor")
def set_motor(req: MotorRequest):
    requested_speed = req.speed
    logger.info(f"Request to change motor speed to: {requested_speed}")
    machine.set_motor_speed(requested_speed)
    return {"speed": machine.snapshot()["motor_speed"]}

# Valve
@app.get("/valve")
def get_valve():
    return {"open": machine.snapshot()["valve_open"]}

@app.post("/valve")
def set_valve(req: ValveRequest):
    machine.update_valve(req.open)
    return {"open": machine.snapshot()["valve_open"]}

# Temperature
@app.get("/temperature")
def get_temp():
    temperature = get_temperature()
    return {"temperature": temperature}