import asyncio
import aiohttp
from datetime import datetime

async def fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def sort(city: dict) -> float:
    now = datetime.now()
    nowaday = now.strftime(f"%d")

    index_of_elems = []

    for i, date in enumerate(city["hourly"]["time"]):
        if date.startswith("2024-10-21"):
            index_of_elems.append(i)


    srednia = 0
    for index in index_of_elems:
        srednia += city["hourly"]["temperature_2m"][index]

    return srednia / len(index_of_elems)

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

    dane2 = await fetch(pogoda2)
    dane2 = {**{"miasto": "Kyiv"}, **dane2}
    dane3 = await fetch(pogoda3)
    dane3 = {**{"miasto": "Argentina"}, **dane3}
    dane4 = await fetch(pogoda4)
    dane4 = {**{"miasto": "Chili"}, **dane4}

    duzo_danych = [dane1, dane2, dane3, dane4]

    sredni = []
    for dane in duzo_danych:
        sredni.append(await sort(dane))

    dane1 = {**{"srednia_tp": sredni[0]}, **dane1}
    dane2 = {**{"srednia_tp": sredni[1]}, **dane2}
    dane3 = {**{"srednia_tp": sredni[2]}, **dane3}
    dane4 = {**{"srednia_tp": sredni[3]}, **dane4}
    duzo_danych = [dane1, dane2, dane3, dane4]

    sorted_dane = sorted(duzo_danych, key=lambda x: x['srednia_tp'], reverse=True)
    for dane in sorted_dane:
        dane.pop('srednia_tp', None)
    print(sorted_dane)


if __name__ == "__main__":
    asyncio.run(main())