from constants import MY_API_KEY, MY_LATITUDE, MY_LONGITUDE
import requests
import os


# Environment variable sourcing
API_KEY = os.getenv("WEATHER_API_KEY", MY_API_KEY)
LAT = os.getenv("LATITUDE", MY_LATITUDE)
LON = os.getenv("LONGITUDE", MY_LONGITUDE)

# OpenWeatherMap URL for weather data calls
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"


# Functions
def get_temperature():
    try:
        response = requests.get(WEATHER_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["main"]["temp"]
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        return None
    