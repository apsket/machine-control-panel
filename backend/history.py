import os
import aiosqlite
import asyncio
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


DB_PATH_DEFAULT = os.path.join(os.path.dirname(__file__), "data", "telemetry.db")


async def init_db(db_path: Optional[str] = None):
    path = db_path or DB_PATH_DEFAULT
    os.makedirs(os.path.dirname(path), exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                motor_actual INTEGER,
                motor_target INTEGER,
                valve_open INTEGER,
                temperature REAL
            )
            """
        )
        await db.execute("CREATE INDEX IF NOT EXISTS idx_ts ON telemetry(ts)")
        await db.commit()
    logger.info("Telemetry DB initialized at %s", path)


async def insert_sample(ts: int, motor_actual: int, motor_target: int, valve_open: bool, temperature: Optional[float], db_path: Optional[str] = None):
    path = db_path or DB_PATH_DEFAULT
    try:
        async with aiosqlite.connect(path) as db:
            await db.execute(
                "INSERT INTO telemetry (ts, motor_actual, motor_target, valve_open, temperature) VALUES (?, ?, ?, ?, ?)",
                (ts, motor_actual, motor_target, int(valve_open), temperature),
            )
            await db.commit()
    except Exception:
        logger.exception("Failed to insert telemetry sample")


async def query_history(start_ts: Optional[int] = None, end_ts: Optional[int] = None, limit: int = 1000, db_path: Optional[str] = None) -> List[Dict]:
    path = db_path or DB_PATH_DEFAULT
    where = []
    params = []
    if start_ts is not None:
        where.append("ts >= ?")
        params.append(start_ts)
    if end_ts is not None:
        where.append("ts <= ?")
        params.append(end_ts)
    where_clause = ("WHERE " + " AND ".join(where)) if where else ""
    # If a time window is provided, return rows in ascending (chronological) order
    # so callers receive time series from oldest->newest. If no window is provided,
    # return the most recent rows (descending) which callers may reverse if needed.
    if where:
        q = f"SELECT ts, motor_actual, motor_target, valve_open, temperature FROM telemetry {where_clause} ORDER BY ts ASC LIMIT ?"
    else:
        q = f"SELECT ts, motor_actual, motor_target, valve_open, temperature FROM telemetry {where_clause} ORDER BY ts DESC LIMIT ?"
    params.append(limit)
    rows = []
    try:
        async with aiosqlite.connect(path) as db:
            async with db.execute(q, params) as cur:
                async for row in cur:
                    rows.append({
                        "ts": row[0],
                        "motor_actual": row[1],
                        "motor_target": row[2],
                        "valve_open": bool(row[3]),
                        "temperature": row[4],
                    })
    except Exception:
        logger.exception("Failed to query telemetry")
    return rows


async def prune_older_than(cutoff_ts: int, db_path: Optional[str] = None):
    """Delete telemetry rows older than cutoff_ts (unix ms)."""
    path = db_path or DB_PATH_DEFAULT
    try:
        async with aiosqlite.connect(path) as db:
            await db.execute("DELETE FROM telemetry WHERE ts < ?", (cutoff_ts,))
            await db.commit()
            logger.debug("Pruned telemetry rows older than %s", cutoff_ts)
    except Exception:
        logger.exception("Failed to prune telemetry")
