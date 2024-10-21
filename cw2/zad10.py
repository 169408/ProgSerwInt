import aiohttp
import asyncio

from aiohttp import request

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            if 200 <= response.status < 300:
                return await response.text()
            else:
                    print(f"Błąd: {response.status} dla {url}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Błąd klienta: {e}")
        return None

async def process_data(data, url):
    if data:
        print(f"Przetwarzanie danych z {url} (długość: {len(data)} znaków)")
        return f"Dane z {url} mają długość: {len(data)} znaków\n"
    else:
        return f"Brak danych do przetworzenia z {url}\n"

async def save_to_file(processed_data):
    if processed_data is not None:
        with open("wyniki.txt", "a") as file:
            file.write(processed_data)

async def send_requests(requests: list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in requests:
            task = fetch(url, session)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        for result in results:
            await save_to_file(result)


async def fetch_and_process(url, session):
    data = await fetch(url, session)
    processed_data = await process_data(data, url)
    return processed_data

if __name__ == "__main__":
    urls = [
        "https://jut.su/naruuto/season-2/episode-375.html",
        "https://github.com/betacord/PSI/blob/main/lectures/2_rest_api.ipynb",
        "https://www.kingston.com/pl/blog/data-security/what-is-encryption"
    ]
    asyncio.run(send_requests(urls))
