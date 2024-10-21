import asyncio
import aiohttp

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main() -> None:
    url1 = "https://670bef0e7e5a228ec1cf1824.mockapi.io/api/v1/user"
    url2 = "https://news.google.com/home?hl=pl&gl=PL&ceid=PL:pl"
    url3 = "https://jsonplaceholder.typicode.com/posts/2"
    url4 = "https://jsonplaceholder.typicode.com/posts/3"
    url5 = "https://jsonplaceholder.typicode.com/posts/4"

    dane1 = await fetch(url1)
    dane2 = await fetch(url2)
    dane3 = await fetch(url3)
    dane4 = await fetch(url4)
    dane5 = await fetch(url5)

    print(dane1)
    print(dane2)
    print(dane3)
    print(dane4)
    print(dane5)

if __name__ == "__main__":
    asyncio.run(main())