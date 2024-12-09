import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
API_BASE_URL = "http://api.openweathermap.org/data/2.5"
DEFAULT_CITY = "Pune"
CURRENT_WEATHER_ENDPOINT = "weather"
FORECAST_ENDPOINT = "forecast"

http_params = {
    "appid": API_KEY,
    "units": "metric"
}