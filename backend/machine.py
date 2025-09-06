from constants import SCAN_INTERVAL, MIN_MOTOR_SPEED, MAX_MOTOR_SPEED, MOTOR_STEP, VALVE_DELAY
import logging
import asyncio


# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,  # minimum level you want to capture
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Machine:
    def __init__(self, min_speed=MIN_MOTOR_SPEED, max_speed=MAX_MOTOR_SPEED):
        logger.info(f"Initializing machine...")
        self.motor_actual_speed = 0
        self.motor_target_speed = 0
        self.valve_open = False
        self.valve_target = False
        self.min_speed = min_speed
        self.max_speed = max_speed

    def set_motor_target(self, speed: int):
        logger.info(f"Target motor speed set to {speed}")
        self.motor_target_speed = max(self.min_speed, min(self.max_speed, speed))

    def set_valve_target(self, open: bool):
        self.valve_target = open

    def step_motor(self, step=MOTOR_STEP):
        old_speed = self.motor_actual_speed
        if self.motor_target_speed > self.motor_actual_speed + step:
            self.motor_actual_speed += step
        elif self.motor_target_speed < self.motor_actual_speed - step:
            self.motor_actual_speed -= step
        else:
            self.motor_actual_speed = self.motor_target_speed
        logger.info(f"Motor speed updated: {old_speed} → {self.motor_actual_speed}")
    
    def is_motor_speed_to_change(self):
        return self.motor_target_speed != self.motor_actual_speed

    def update_valve(self):
        self.valve_open = self.valve_target
    
    def is_valve_to_change(self):
        return self.valve_target != self.valve_open

    def snapshot(self):
        return {
            "motor_actual_speed": self.motor_actual_speed,
            "motor_target_speed": self.motor_target_speed,
            "valve_open": self.valve_open,
            "valve_target": self.valve_target,
        }


class PLC:
    def __init__(self, machine: Machine, scan_interval=SCAN_INTERVAL, motor_step=MOTOR_STEP, valve_delay=VALVE_DELAY):
        self.machine = machine
        self.scan_interval = scan_interval
        self.motor_step = motor_step
        self.valve_delay = valve_delay

    async def run(self):
        while True:
            logger.debug("Starting PLC scan cycle...")
            if self.machine.is_motor_speed_to_change():
                self.machine.step_motor(self.motor_step)
            if self.machine.is_valve_to_change():
                await asyncio.sleep(self.valve_delay)
                self.machine.update_valve()
            logger.debug(f"PLC scan complete: Motor={self.machine.motor_actual_speed}, Valve={self.machine.valve_open}")
            await asyncio.sleep(self.scan_interval)
