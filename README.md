# Machine Control Panel

Summary: Full-stack application with web-based dashboard for monitoring and control of motor speed, valve, and ambient temperature sensor (fetched from OpenWeatherMap API) in real time. Built with React on the frontend and communicates with a backend API for hardware control.

The code in this branch `feature/transition-gradual` simulates some characteristics of physical systems such as a finite rate of change of motor speed and a non-null time interval to toggle the valve state. This was implemented in the backend with the use of asynchronous tasks through the `asycio` Python. For a simpler version of the project where values are updated immediately after changes are requested refer to the `feature/transition-immediate` branch of the present repository.

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

All backend constants are defined in `backend/constants.py`. The frontend polls motor speed and valve states from the backend every 200 ms.

Changes to the motor speed and valve state are sent through the web dashboard to the backend. A PLC-like behavior then constantly loops reading the desired target state and applying the rate-limited changes each cycle. This is done asynchronously to simulate waiting times and allow the frontend to specify the desired changes independently. A delay `SCAN_INTERVAL` (in seconds) is defined for the PLC scanning loop.

### Motor Control
Values of motor speed are specified in arbitrary units, though they could be understood to be in `RPM`. Values of motor speed are limited to integers in the closed interval `[MIN_MOTOR_SPEED, MAX_MOTOR_SPEED]`. If a value outside of this range is input, the system will assign the motor speed to the closest of the interval boundary points. Values of motor speed are changed in at most `MOTOR_STEP` units per PLC cycle.

### Valve Control
The valve toggling has a time delay between times of requested and applied changes. This is controlled by the `VALVE_DELAY` variable.

### Temperature Display
Temperature is fetched in real-time from OpenWeatherMap's API. This service provider was selected because of its known stability and sufficiency of its free tier offerings. Free tier allows 60 API calls/minute, not exceeding 1,000,000 API calls/month (https://openweathermap.org/full-price#current). The temperature is fetched every 2 minutes. OpenWeatherMap suggests “... making API calls no more than once in 10 minutes for each location, whether you call it by city name, geographical coordinates or by zip code. The update frequency of the OpenWeather model is not higher than once in 10 minutes.” (https://openweathermap.org/appidUpdates). The key to call OpenWeatherMap's free API is defined by `MY_API_KEY`. The location for real-time temperature data is defined by `MY_LATITUDE` and `MY_LONGITUDE`. As of the most recent commit, this location corresponds to approximately the 66260 zip code in San Pedro Garza Garcia, Nuevo Leon, Mexico.

## How to Run

This project is configured to run in a local development environment. This approach was chosen to simplify the setup process and to focus on the core requirements of the task.

### Starting the Backend:
1.	Clone the repository to your local machine and navigate into the cloned project directory::
```
git clone https://github.com/apsket/machine-control-panel.git
cd <your-cloned-project-folder>
```
2. Ensure you are checkout out at the correct branch `feature/transition-gradual`:
```
git checkout feature/transition-gradual
```

4. Navigate to the `backend` directory of the cloned repo and install the requirements in a clean python environment (ideally with Python 3.12.11):
 ```
pip install -r requirements.txt
```
4. Run the backend:
 ```
uvicorn app:app --reload
```
This will start the backend API server on `http://127.0.0.1:8000`.

### Starting the Frontend
5. In a new terminal window, navigate to the `frontend` directory to install and then run:
 ```
npm install
npm run dev
```
This will start the React development server, it should be available at `http://localhost:5173`.

Note: For a production environment, a more robust setup would be used, such as a WSGI server like Gunicorn for the backend and a static file server for the frontend.

### Using the Web App
6. Open a window of the web browser of your choice and go to the URL defined by the output of the frontend run command (typically should be `http://localhost:5173`). You should now be able to use the web UI to apply changes and see the system's behavior.


## Future Improvements

### Environment Variables
The current project uses hardcoded values for API endpoints. A better practice for production is to use environment variables (e.g., VITE_API_URL for the frontend and .env files for the backend). This separates sensitive information and configuration from the source code, making the application more portable and secure. The backend and frontend can read these variables at runtime, allowing the application to be deployed in different environments without code changes.

### Containerization with Docker
Containerizing the application with Docker and Docker Compose would standardize the deployment environment. It ensures that the application, along with its dependencies (Python, Node.js), runs consistently on any system. A Dockerfile for each service (frontend and backend) would define the build environment, and a single docker-compose.yml file would manage both services together. This simplifies the setup process for other developers and for deployment to cloud platforms. (See the branch `feature/transition-gradual-DOCKER` for progress in containerizing the app.)

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
