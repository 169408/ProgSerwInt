from dependency_injector.wiring import Provide

import asyncio

from container import Container
from services.ipost_service import IPostService
from utils import consts


async def main(
        service: IPostService = Provide[Container.service],
) -> None:

    await service.fetch_and_cache_posts()


    print("Pobrano wszystkie posty i zapisano w pamięci.")

    search_query = "maiores"
    filtered_posts = service.filter_posts(search_query)
    print(f"Posty zawierające '{search_query}':")
    for post in filtered_posts:
        print(post)


    all_posts_json = service.get_all_posts_as_json()
    print("Wszystkie posty w formacie JSON:")
    print(all_posts_json)



if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())