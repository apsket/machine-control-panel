from settings import settings
import httpx
import asyncio
import time
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)


# Simple in-memory TTL cache for temperature
_temp_cache = {"value": None, "ts": 0}
_cache_lock = asyncio.Lock()


class HTTPError(Exception):
    pass


@retry(reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10),
       retry=retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError, HTTPError)))
async def _fetch_temperature_from_api():
    api_key = settings.WEATHER_API_KEY
    if not api_key:
        raise HTTPError("WEATHER_API_KEY not set in environment; cannot fetch temperature")

    lat = settings.LATITUDE
    lon = settings.LONGITUDE
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    timeout = httpx.Timeout(5.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(weather_url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("main", {}).get("temp")


async def get_temperature():
    """Return cached temperature and timestamp if fresh, otherwise fetch from API with retries.

    Returns dict: {"temperature": float|None, "timestamp": ISO8601 str|None}
    """
    ttl = settings.WEATHER_CACHE_TTL
    now = time.time()

    async with _cache_lock:
        if _temp_cache["value"] is not None and (now - _temp_cache["ts"]) < ttl:
            ts = datetime.fromtimestamp(_temp_cache["ts"], tz=timezone.utc).isoformat()
            logger.debug("Returning cached temperature (ts=%s) ttl=%s", ts, ttl)
            return {"temperature": _temp_cache["value"], "timestamp": ts}

    try:
        logger.info("Fetching temperature from external API")
        temp = await _fetch_temperature_from_api()
    except Exception as e:
        # On failure, return cached value if present, else None
        async with _cache_lock:
            if _temp_cache["value"] is not None:
                ts = datetime.fromtimestamp(_temp_cache["ts"], tz=timezone.utc).isoformat()
                logger.warning("Failed to fetch temperature, returning cached value: %s", e)
                return {"temperature": _temp_cache["value"], "timestamp": ts}
        logger.error("Error fetching temperature: %s", e)
        return {"temperature": None, "timestamp": None}

    async with _cache_lock:
        _temp_cache["value"] = temp
        _temp_cache["ts"] = time.time()
        ts = datetime.fromtimestamp(_temp_cache["ts"], tz=timezone.utc).isoformat()
        logger.info("Updated temperature cache: %s", temp)

    return {"temperature": temp, "timestamp": ts}
    