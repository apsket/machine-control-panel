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

## Installation
	1.	Clone the repository to your local machine:
```
gh repo clone apsket/machine-control-panel
cd <your-cloned-repo-folder>
```

## Future Improvements

Environment variables defined for both frontend and backend defined as environment variables at the project root... containerization of the application through docker and docker-compose (see the branch `feature/transition-gradual-DOCKER` for a non-stable progress of such containerization)... port selection... improved logging... machine state persistency simulation by saving state to file or using a lightweight database... unit testing... dependency injection... implement authentication
    
