from settings import settings
import requests


def get_temperature():
    """Fetch current temperature from OpenWeatherMap using configured settings.

    Returns temperature in Celsius or `None` if unavailable.
    """
    api_key = settings.WEATHER_API_KEY
    if not api_key:
        print("WEATHER_API_KEY not set in environment; cannot fetch temperature")
        return None

    lat = settings.LATITUDE
    lon = settings.LONGITUDE
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(weather_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["main"]["temp"]
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        return None
    