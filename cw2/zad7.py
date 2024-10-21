import asyncio
from cgi import print_form

import aiohttp

async def download(url: str, save_path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()

                with open(save_path, 'wb') as file:
                    file.write(content)
                print(f"Pobrano plik i zapisano w {save_path}")
            else:
                print(f"Nie udało się pobrać plik")


async def main():
    url = "https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/03/seraph-of-the-end-season-3.jpg"

    save_path = "pliki/pobrany_plik.jpg"

    await download(url, save_path)


if __name__ == "__main__":
    asyncio.run(main())