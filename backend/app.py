from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from services import get_temperature

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
    "motor_speed": MIN_MOTOR_SPEED,
    "valve_open": False
}

# -----------------------------
# Endpoints
# -----------------------------

# Motor
@app.get("/motor")
def get_motor():
    return {"speed": machine_state["motor_speed"]}

@app.post("/motor")
def set_motor(req: MotorRequest):
    requested_speed = req.speed
    machine_state["motor_speed"] = max(MIN_MOTOR_SPEED, min(MAX_MOTOR_SPEED, requested_speed))
    return {"speed": machine_state["motor_speed"]}

# Valve
@app.get("/valve")
def get_valve():
    return {"open": machine_state["valve_open"]}

@app.post("/valve")
def set_valve(req: ValveRequest):
    machine_state["valve_open"] = req.open
    return {"open": machine_state["valve_open"]}

# Temperature
@app.get("/temperature")
def get_temp():
    temperature = get_temperature()
    return {"temperature": temperature}