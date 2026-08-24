from typing import Optional
from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


# Load .env from repository root if present
repo_root_env = Path(__file__).resolve().parents[1] / ".env"
env_path = str(repo_root_env) if repo_root_env.exists() else str(Path(__file__).resolve().parent / ".env")
if load_dotenv:
    load_dotenv(env_path)


def _getenv(key: str, default=None):
    return os.getenv(key, default)


class Settings:
    # External API / secrets
    WEATHER_API_KEY: Optional[str] = _getenv("WEATHER_API_KEY")

    # Location (can be overridden by env)
    LATITUDE: str = _getenv("LATITUDE", "25.6571")
    LONGITUDE: str = _getenv("LONGITUDE", "-100.348")

    # Machine tuning defaults
    MIN_MOTOR_SPEED: int = int(_getenv("MIN_MOTOR_SPEED", "0"))
    MAX_MOTOR_SPEED: int = int(_getenv("MAX_MOTOR_SPEED", "100"))
    MOTOR_STEP: int = int(_getenv("MOTOR_STEP", "3"))
    SCAN_INTERVAL: float = float(_getenv("SCAN_INTERVAL", "0.1"))
    VALVE_DELAY: float = float(_getenv("VALVE_DELAY", "2.0"))

    # App / deployment
    CORS_ORIGINS: str = _getenv("CORS_ORIGINS", "http://localhost:5173")
    LOG_LEVEL: str = _getenv("LOG_LEVEL", "INFO")
    # Weather API cache TTL in seconds (lowered for dev/debugging)
    WEATHER_CACHE_TTL: int = int(_getenv("WEATHER_CACHE_TTL", "30"))
    # Telemetry retention in milliseconds (default 10 minutes)
    # Telemetry retention in milliseconds (default 10 minutes)
    TELEMETRY_RETENTION_MS: int = int(_getenv("TELEMETRY_RETENTION_MS", str(10 * 60 * 1000)))
    # Default window for telemetry charts (ms). Frontend can request this via /config.
    TELEMETRY_WINDOW_MS: int = int(_getenv("TELEMETRY_WINDOW_MS", str(5 * 60 * 1000)))
    # How often to run pruning (seconds)
    TELEMETRY_PRUNE_INTERVAL: int = int(_getenv("TELEMETRY_PRUNE_INTERVAL", "60"))


settings = Settings()
