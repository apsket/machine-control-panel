from constants import MIN_MOTOR_SPEED, MAX_MOTOR_SPEED
import logging


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
        self.motor_speed = MIN_MOTOR_SPEED
        self.valve_open = False
        self.min_speed = min_speed
        self.max_speed = max_speed

    def set_motor_speed(self, speed: int):
        self.motor_speed = max(self.min_speed, min(self.max_speed, speed))
        logger.info(f"Motor speed set to {speed}")

    def update_valve(self, valve_target):
        self.valve_open = valve_target

    def snapshot(self):
        return {
            "motor_speed": self.motor_speed,
            "valve_open": self.valve_open
        }


