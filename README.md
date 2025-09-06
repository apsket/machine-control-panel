# Machine Control Panel

Summary: Full-stack application with web-based dashboard for monitoring and control of motor speed, valve, and ambient temperature sensor (fetched from OpenWeatherMap API) in real time. Built with React on the frontend and communicates with a backend API for hardware control.

The code in this branch `feature/transition-gradual` simulates some characteristics of physical systems such as a finite rate of change of motor speed and a non-null time interval to toggle the valve state. This was implemented in the backend with the use of asynchronous tasks through the `asycio` Python.

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

All backend constants are defined in `backend/constants.py`.

Changes to the motor speed and valve state are sent through the web dashboard to the backend. A PLC-like behavior then constantly loops reading the desired target state and applying the rate-limited changes each cycle. This is done asynchronously to simulate waiting times and allow the frontend to specify the desired changes independently. A delay `SCAN_INTERVAL` (in seconds) is defined for the PLC scanning loop.

### Motor Control
Values of motor speed are specified in arbitrary units, though they could be understood to be in `RPM`. Values of motor speed are limited to integers in the closed interval `[MIN_MOTOR_SPEED, MAX_MOTOR_SPEED]`. If a value outside of this range is input, the system will assign the motor speed to the closest of the interval boundary points. Values of motor speed are changed in at most `MOTOR_STEP` units per PLC cycle.

### Valve Control
View current valve state (Open/Closed). Toggle valve state. Displays 'Changing to … message' until the valve reaches the target. Allows overriding the target while changing.

### Temperature Display
Shows the latest temperature reading from the backend. Updates every 2 minutes. Real-time Updates. Polls motor speed and valve state every 200ms. Automatic display updates for changing states.

### Responsive UI
Minimal, clean design. Compact control panels for each component. Built with TailwindCSS for styling.

Installation
	1.	Clone the repository:
    