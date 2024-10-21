import asyncio
import aiohttp

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main() -> None:
    polmar = "https://api.open-meteo.com/v1/forecast?latitude=10.9577&longitude=-63.8697&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    #moroni = "https://open-meteo.com/en/docs#latitude=-11.7022&longitude=43.2551"
    #helsinek = "https://open-meteo.com/en/docs#latitude=56.0228&longitude=12.1975"

    dane = await fetch(polmar)
    #dane2 = await fetch(moroni)
    #dane3 = await fetch(helsinek)
    print(dane)
    #print(dane2)
    #print(dane3)

if __name__ == "__main__":
    asyncio.run(main())