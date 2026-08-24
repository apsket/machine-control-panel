# Machine Control Panel

**Built a full-stack control dashboard simulating real-world system behavior, using AI-assisted development to rapidly implement a React frontend and asynchronous backend logic.**

Full-stack application with web-based dashboard for monitoring and control of motor speed, valve, and ambient temperature sensor (fetched from OpenWeatherMap API) in real time. Built with React on the frontend and communicates with a backend API for hardware control.

The code in this branch `feature/transition-gradual` simulates some characteristics of physical systems such as a finite rate of change of motor speed and a non-null time interval to toggle the valve state. This was implemented in the backend with the use of asynchronous tasks through the `asycio` Python. For a simpler version of the project where values are updated immediately after changes are requested refer to the `feature/transition-immediate` branch of the present repository.

## Product Capabilities

- Monitor and control system components (motor speed, valve state) in real time.
- Handle delayed and rate-limited state transitions, reflecting real-world system constraints.
- Override in-progress actions, enabling dynamic control under changing conditions.
- Visual feedback for system state changes (“changing to…”) to improve user understanding.
- Live environmental data integration (temperature via external API).

## Product & System Design Considerations

- Modeled realistic system behavior (rate limits, delays) instead of instant state changes.
- Designed UI feedback to reflect intermediate states and avoid misleading users.
- Allowed user overrides during transitions to simulate real operator workflows.
- Balanced polling frequency (200ms) with responsiveness and system load.

## AI-Assisted Development

- Used AI tools to accelerate frontend development (React, Tailwind), enabling rapid implementation despite limited prior experience.
- Leveraged AI for debugging, design iteration, and exploring implementation alternatives.
- Focused on validating behavior and system logic rather than manual implementation details.
  
## Features Overview

	•	Motor Control
	    •	View current motor speed.
	    •	Set a new target speed.
	    •	Displays 'Changing to …' message while the motor adjusts.
	    •	Allows overwriting the target speed while changing.
	•	Valve Control
	    •	View current valve state (Open/Closed).
	    •	Toggle valve state.
	    •	Displays 'Changing to … message' until the valve reaches the target.
	    •	Allows overriding the target while changing.
	•	Temperature Display
	    •	Shows the latest temperature reading from the backend.
	    •	Updates every 2 minutes.
	•	Real-time Updates
	    •	Polls motor speed and valve state every 200ms.
	    •	Automatic display updates for changing states.
	•	Responsive UI
	    •	Minimal, clean design.
	    •	Compact control panels for each component.
	    •	Built with TailwindCSS for styling.

## Implementation Details

The system is designed to simulate control behavior found in physical systems, using asynchronous backend processes and continuous state evaluation loops.

All backend constants are defined in `backend/constants.py`. The frontend polls motor speed and valve states from the backend every 200 ms.

Changes to the motor speed and valve state are sent through the web dashboard to the backend. A PLC-like behavior then constantly loops reading the desired target state and applying the rate-limited changes each cycle. This is done asynchronously to simulate waiting times and allow the frontend to specify the desired changes independently. A delay `SCAN_INTERVAL` (in seconds) is defined for the PLC scanning loop.

### Motor Control
Values of motor speed are specified in arbitrary units, though they could be understood to be in `RPM`. Values of motor speed are limited to integers in the closed interval `[MIN_MOTOR_SPEED, MAX_MOTOR_SPEED]`. If a value outside of this range is input, the system will assign the motor speed to the closest of the interval boundary points. Values of motor speed are changed in at most `MOTOR_STEP` units per PLC cycle.

### Valve Control
The valve toggling has a time delay between times of requested and applied changes. This is controlled by the `VALVE_DELAY` variable.

### Temperature Display
Temperature is fetched in real-time from OpenWeatherMap's API. This service provider was selected because of its known stability and sufficiency of its free tier offerings. Free tier allows 60 API calls/minute, not exceeding 1,000,000 API calls/month (https://openweathermap.org/full-price#current). The temperature is fetched every 2 minutes. OpenWeatherMap suggests “... making API calls no more than once in 10 minutes for each location, whether you call it by city name, geographical coordinates or by zip code. The update frequency of the OpenWeather model is not higher than once in 10 minutes.” (https://openweathermap.org/appidUpdates). The key to call OpenWeatherMap's free API is defined by `MY_API_KEY`. The location for real-time temperature data is defined by `MY_LATITUDE` and `MY_LONGITUDE`. As of the most recent commit, this location corresponds to approximately the 66260 zip code in San Pedro Garza Garcia, Nuevo Leon, Mexico.

## How to Run

This project provides two ways to run the full application locally. The recommended and primary method is Docker Compose (reproducible, fast to start). A local developer workflow is also included below for iterative development.

### Recommended (primary): Docker Compose
1. Copy the example env file to the repository root and set your OpenWeatherMap API key:
```bash
cp backend/.env.example .env
# edit .env and set WEATHER_API_KEY=your_openweathermap_api_key_here
```
2. Build and start both services:
```bash
docker compose build
docker compose up -d
```
3. Open the app in your browser:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
4. Stop and remove containers when finished:
```bash
docker compose down
```

### Developer (optional): Local development without Docker
Use this workflow for iterative development and debugging.

Backend (Poetry - recommended):
```bash
cd backend
cp .env.example .env
# install dependencies
poetry install
# run local server
poetry run uvicorn app:app --reload --port 8000
```

Backend (pip / venv alternative):
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Frontend (Vite):
```bash
cd frontend
npm install
npm run dev
```

### Quick API checks
You can exercise the API with curl while the server is running, for example:
```bash
curl http://127.0.0.1:8000/motor
curl -X POST http://127.0.0.1:8000/motor -H 'Content-Type: application/json' -d '{"speed":60}'
```

## Future Improvements

### Limitations
The system has a number of features that could be modified for a nicer user experience. For instance, the minimum and maximum values for motor speed are not shown in the UI. Target speeds are inserted numerically in a UI box. To make the bounded nature of speeds explicit, an input slider would be useful. A slider reflecting the actual motor speed could be a nice feature to add as well. When a target valule lies outside of the allowed range for motor speed, the UI will forever display the message 'Changing to `target_speed`...' even after the motor speed stabilizes at the minimum or maximum allowed value. It would be better to remove the changing state message once the motor speed stabilizes.

With regards to the ambient temperature. Currently the latitude and longitude variables are defined as constants in the backend and they are not shown in the dashboard. One could have them displayed and even changed by the user at the UI level. OpenWeather also offers other APIs such as the Geocoding API that returns details such as latitude and longitude from a request with zip code and country code as parameters (https://openweathermap.org/api/geocoding-api). This would allow the user more flexibility in changing the ambient temperature.

### Port Selection
Currently, the application uses hardcoded ports (3000 and 8000). For a production environment, it would be beneficial to make these ports configurable through environment variables. This prevents port conflicts on a server where multiple applications may be running.

### Improved Logging
Implementing a more robust logging system would be crucial for monitoring and debugging. The current console.error calls are not suitable for production. A professional setup would involve using a logging library to capture detailed information about application events, errors, and performance metrics. These logs can then be centralized for analysis, helping to identify and resolve issues more efficiently.

### Machine State Persistency
The machine's state (motor speed and valve state) is currently stored in memory and resets when the backend server restarts. To simulate state persistency, you could save the state to a lightweight file (like a JSON file) or a simple, embedded database (such as SQLite). The backend would read the state from the file on startup and write to it whenever a change occurs.

### Unit Testing
Adding unit tests would ensure the reliability of the application's core logic. For the backend, tests would verify that API endpoints function as expected and that the machine simulation logic is correct. For the frontend, tests would validate that components render correctly and user interactions work as intended. This practice is essential for maintaining code quality and preventing regressions.

### System State Plots
Adding plots to the dashboard would provide a visual representation of the machine's state over time. You could use a charting library (like Chart.js or D3.js) on the frontend to display a live graph of motor speed or temperature over the most recent time window. This adds a valuable monitoring feature for operators.

	
## Final Note
Remember you can access a simpler and stable version of the project available in the branch `feature/transition-immediate`.
