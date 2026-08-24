from settings import settings
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
    def __init__(self, min_speed=settings.MIN_MOTOR_SPEED, max_speed=settings.MAX_MOTOR_SPEED):
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

    def step_motor(self, step=settings.MOTOR_STEP):
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
    def __init__(self, machine: Machine, scan_interval=settings.SCAN_INTERVAL, motor_step=settings.MOTOR_STEP, valve_delay=settings.VALVE_DELAY):
        self.machine = machine
        self.scan_interval = scan_interval
        self.motor_step = motor_step
        self.valve_delay = valve_delay
        self._valve_task = None

    async def _do_valve_transition(self):
        logger.info(f"Starting valve transition task (delay={self.valve_delay}s)")
        await asyncio.sleep(self.valve_delay)
        # Apply whichever target is current at the time the delay finishes
        self.machine.update_valve()
        logger.info(f"Valve transition complete: open={self.machine.valve_open}")

    async def run(self):
        while True:
            logger.debug("Starting PLC scan cycle...")
            # Motor stepping remains fast and independent
            if self.machine.is_motor_speed_to_change():
                self.machine.step_motor(self.motor_step)

            # Valve transitions run asynchronously so they don't block motor stepping
            if self.machine.is_valve_to_change():
                # start a background task if one isn't already running
                if self._valve_task is None or self._valve_task.done():
                    self._valve_task = asyncio.create_task(self._do_valve_transition())
            logger.debug(f"PLC scan complete: Motor={self.machine.motor_actual_speed}, Valve={self.machine.valve_open}")
            await asyncio.sleep(self.scan_interval)
