import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone

async def fetch_weather(city: str, lattitude: float, longtude: float) -> dict:
    url = ("https://api.open-meteo.com/v1/forecast?latitude=10.9577&longitude=-63.8697&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


def get_closest_hour_forecast(weather_data: dict) -> dict:
    # Pobieramy prognozy godzinowe
    hourly_data = weather_data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    humidity = hourly_data.get("relative_humidity_2m", [])
    wind_speed = hourly_data.get("wind_speed_10m", [])

    #Znajdź najbliższą godzinę
    now = datetime.now()
    print(now)
    next_full_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    print(next_full_hour)

    # Zakładamy, że pierwsza godzina to najbliższa godzina (można dostosować dla bardziej zaawansowanych funkcji)
    # if times and temperatures and humidity and wind_speed:
    #     return {
    #         "time": times[0],  # Najbliższa godzina
    #         "temperature": temperatures[0],
    #         "humidity": humidity[0],
    #         "wind_speed": wind_speed[0],
    #     }
    for i, forecast_time in enumerate(times):
        forecast_datetime = datetime.fromisoformat(forecast_time)
        if(forecast_datetime >= next_full_hour):
            return {
                "time": forecast_time,
                "temperature": temperatures[i],
                "humidity": humidity[i],
                "wind_speed": wind_speed[i],
            }

    return {}

async def get_weather_for_cities() -> dict:
    cities = {
        "Porlamar": {"latitude": 10.9577, "longitude": -63.8697},
        "Moroni": {"latitude": -11.7022, "longitude": 43.2551},
        "Helsinki": {"latitude": 60.1695, "longitude": 24.9354}
    }

    # Tworzymy zadania asynchroniczne dla każdego miasta
    tasks = [fetch_weather(city, data["latitude"], data["longitude"]) for city, data in cities.items()]
    weather_data = await asyncio.gather(*tasks)

    # Tworzymy słownik wyników z prognozą dla najbliższej godziny
    result = {}
    for city, data in zip(cities.keys(), weather_data):
        result[city] = get_closest_hour_forecast(data)

    return result


if __name__ == "__main__":
    weather_forecast = asyncio.run(get_weather_for_cities())
    print(weather_forecast)
