from dependency_injector.wiring import Provide

import asyncio

from container import Container
from services.ipost_service import IPostService
from utils import consts
from utils.cleanup_task import periodic_cleanup


async def main(
        service: IPostService = Provide[Container.service],
) -> None:

    await service.load_data()

    asyncio.create_task(periodic_cleanup(service, interval=61, threshold=50))

    filtered_posts = service.filter_posts("odio adipisci")
    sorted_posts = service.sort_by_last_used()

    print(filtered_posts)
    await asyncio.sleep(5)
    print(service._posts_cache)
    await asyncio.sleep(60)
    print("Last")
    print("Last")
    print("Last")
    print("Last")
    print("Last")
    print("Last")
    print("Last")
    print(service._posts_cache)
    #print(sorted_posts)



if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())