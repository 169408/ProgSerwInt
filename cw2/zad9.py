import aiohttp
import asyncio


async def fetch_with_retry(url, session, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            async with session.get(url) as response:
                if 200 <= response.status < 300:
                    return await response.text()  # Zwracamy tylko poprawne odpowiedzi
                elif 500 <= response.status < 600:
                    retries += 1
                    print(f"Server error ({response.status}). Retrying {retries}/{max_retries}...")
                else:
                    # Odpowiedzi spoza zakresu 200-299 i 500-599 są ignorowane
                    return None
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
            return None
    return None


async def send_requests(url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(100):
            task = fetch_with_retry(url, session)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # Filtrowanie odpowiedzi, które nie są None
        valid_responses = [response for response in responses if response is not None]
        return valid_responses


# Uruchamianie programu
if __name__ == "__main__":
    url = "https://music.youtube.com/watch?v=N3047biRZzI&list=PLc6TGDUYOST5J289iW4496pCFFQkzdxps"  # Przykładowy REST API
    valid_responses = asyncio.run(send_requests(url))

    print(f"Received {len(valid_responses)} valid responses out of 100 requests.")