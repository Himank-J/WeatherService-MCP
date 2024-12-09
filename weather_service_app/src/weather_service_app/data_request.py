import requests
import datetime
from typing import Any
from config import API_BASE_URL, FORECAST_ENDPOINT, http_params

async def fetch_weather(city: str) -> dict[str, Any]:

    response = requests.get(
        f"{API_BASE_URL}/weather",
        params={"q": city, **http_params}
    )
    response.raise_for_status()
    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "conditions": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.now().isoformat()
    }

async def fetch_forecaset(city: str, days: int) -> list[dict, Any]:
    
    response = requests.get(
        f"{API_BASE_URL}/{FORECAST_ENDPOINT}",
        params={"q": city, "cnt": days * 8, **http_params}
    )
    response.raise_for_status()
    data = response.json()

    forecasts = []
    for i in range(0, len(data["list"]), 8):
        day_data = data["list"][i]
        forecasts.append({
            "date": day_data["dt_txt"].split()[0],
            "temperature": day_data["main"]["temp"],
            "conditions": day_data["weather"][0]["description"]
        })
        
    return forecasts