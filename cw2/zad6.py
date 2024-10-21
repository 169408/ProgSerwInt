import asyncio
import aiohttp

async def fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def validation(city: dict, mask: dict) -> dict:
    wind_speeds = city["hourly"]["wind_speed_10m"]
    curr_temperature = city["current"]["temperature_2m"]
    #print(city.keys())
    for i, wind_speed in enumerate(wind_speeds):
        if "wind_speed_10m" in mask and not eval(f"{wind_speed} {mask['wind_speed_10m']}"):
            return False

    if "temperature_2m" in mask and not eval(f"{curr_temperature} {mask['temperature_2m']}"):
        return False

    return True
    #print(city["hourly"].keys())

async def main() -> dict:
    # Olsztyn
    pogoda1 = "https://api.open-meteo.com/v1/forecast?latitude=53.7799&longitude=20.4942&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    # Kyiv
    pogoda2 = "https://api.open-meteo.com/v1/forecast?latitude=50.4547&longitude=30.5238&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    # Argentina
    pogoda3 = "https://api.open-meteo.com/v1/forecast?latitude=-34&longitude=-64&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    # Chili
    pogoda4 = "https://api.open-meteo.com/v1/forecast?latitude=44.6269&longitude=-90.3565&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    dane1 = await fetch(pogoda1)
    dane1 = {**{"miasto": "Olsztyn"}, **dane1}
    mask = {
        "temperature_2m": "< 9",
        "wind_speed_10m": "< 17"
    }

    dane2 = await fetch(pogoda2)
    dane2 = {**{"miasto": "Kyiv"}, **dane2}
    dane3 = await fetch(pogoda3)
    dane3 = {**{"miasto": "Argentina"}, **dane3}
    dane4 = await fetch(pogoda4)
    dane4 = {**{"miasto": "Chili"}, **dane4}

    duzo_danych = [dane1, dane2, dane3, dane4]

    for dane in duzo_danych:
        if(await validation(dane, mask)):
            print(dane)

if __name__ == "__main__":
    asyncio.run(main())