# Machine Control Panel

A small full-stack demo app that simulates a physical machine (motor + valve) and exposes a React dashboard for control and telemetry. This repository contains a FastAPI backend and a Vite + React frontend with live charts.

Key behaviors:
- Motor: integer target speed, rate-limited ramping (`MOTOR_STEP`) applied each PLC scan.
- Valve: toggles with a configurable delay (`VALVE_DELAY`) implemented as an async transition task.
- Temperature: fetched from OpenWeatherMap using async `httpx` with retries (`tenacity`) and a short in-memory TTL cache.
- Telemetry: each PLC scan inserts timestamped samples into an on-disk SQLite DB (`backend/data/telemetry.db`). A background prune loop removes old samples based on `TELEMETRY_RETENTION_MS`.

**Status:** working — UI displays live charts, controls behave independently, telemetry persists and prunes, and temperature uses a resilient fetch strategy.

---

**Contents**
- Backend: FastAPI app, PLC simulation, telemetry persistence (SQLite), temperature service.
- Frontend: React + Vite, Tailwind CSS, Chart.js (react-chartjs-2) charts per control.
- Dev: Docker Compose setup for running backend + frontend together.

## Features
- Motor control (set target speed; motor ramps toward target at `MOTOR_STEP` per scan).
- Valve control (toggle with `VALVE_DELAY`, supports overriding target while transitioning).
- Ambient temperature from OpenWeatherMap (cached, retried on failure).
- Telemetry history saved to SQLite and exposed by `/history` for plotting and analysis.
- Charts for motor (actual vs target), valve state, and temperature; charts poll backend every 5s and plot a configured time window.

## Important runtime/config options
All environment variables may be set in an `.env` file loaded by the backend. Defaults are listed in `backend/settings.py`.

Notable settings (defaults):
- `WEATHER_API_KEY` - OpenWeatherMap API key (required for live temperature fetching).
- `SCAN_INTERVAL` - PLC scan sleep interval in seconds (default `0.1`).
- `MOTOR_STEP` - motor step per scan (default `3`).
- `VALVE_DELAY` - seconds the valve transition waits before applying target (default `2.0`).
- `WEATHER_CACHE_TTL` - weather cache TTL in seconds (default `30`).
- `TELEMETRY_RETENTION_MS` - how long telemetry is kept (ms, default 10 minutes).
- `TELEMETRY_WINDOW_MS` - default chart window requested by the frontend (ms, default 5 minutes).

## Backend endpoints
- `GET /motor` — current motor state and bounds.
- `POST /motor` — set motor target `{ "speed": <int> }`.
- `GET /valve` — current valve state.
- `POST /valve` — set valve target `{ "open": true|false }`.
- `GET /temperature` — returns `{ temperature, timestamp }` from the cached fetcher.
- `GET /history?start=<ms>&end=<ms>&limit=<n>` — telemetry samples between `start` and `end` (unix ms). When a time window is supplied the results are chronological (oldest→newest). If no window is supplied the most-recent samples are returned (newest-first).
- `GET /config` — small runtime config object `{ telemetry_window_ms }` used by the frontend as a default.

Telemetry schema (SQLite `telemetry` table): `id, ts, motor_actual, motor_target, valve_open, temperature`.

## Running
Two supported workflows: Docker Compose (recommended) and local development.

### 1) Docker Compose (recommended)
1. Copy or create an `.env` with at least your OpenWeatherMap key. Example (project root):
```bash
# create a root .env that the backend image reads via docker-compose
# example content (do not commit secrets):
# WEATHER_API_KEY=your_openweathermap_api_key
```
2. Build and start services:
```bash
docker compose up --build -d
```
3. Visit the UI:
- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

Stop and remove containers when done:
```bash
docker compose down
```

### 2) Local development (no Docker)
Backend (venv/pip):
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ensure .env exists in backend/ or repo root with WEATHER_API_KEY
uvicorn app:app --reload --port 8000
```
Frontend (Vite):
```bash
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

Notes: the frontend in Docker is built and served as a static bundle; the dev server runs on the same port by default for local testing.

## Design notes & rationale
- Telemetry is persisted to SQLite for a simple demo-grade durability and easy inspection (`backend/data/telemetry.db`).
- The backend runs a prune loop that deletes samples older than `TELEMETRY_RETENTION_MS` to limit DB growth.
- The frontend requests a default telemetry window from `/config` (`TELEMETRY_WINDOW_MS`) so the window can be configured without rebuilding the frontend.
- Charts poll every 5s for fresh data; the backend sampling (PLC) is much faster (default 0.1s) so charts see many samples per window. The frontend `limit` can be adjusted if you sample extremely frequently.

## Troubleshooting
- If charts appear stale after a deploy, hard-refresh the browser and verify the API `/config` returns the expected `telemetry_window_ms` value.
- If the frontend still shows the old bundle after a container rebuild, rebuild the frontend image with `--no-cache`:
```bash
docker compose build --no-cache frontend
docker compose up -d
```
- Telemetry DB path: `backend/data/telemetry.db`.

## Development suggestions
- Add server-side downsampling/aggregation for long windows to reduce payload sizes.
- Add API tests for telemetry queries and PLC behavior.
- Persist machine state if you want true restart resilience.

---

If anything here is out of date with the state you're seeing, tell me which section to expand or adjust and I'll update it.