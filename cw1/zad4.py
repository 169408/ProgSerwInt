import asyncio
import random



async def main() -> None:  # 1
    while True:
        print(random.randint(1, 5))
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_task(main())  # 2

    try:
        loop.run_until_complete(task)  # 3
    except KeyboardInterrupt:  # 4
        print("Closing the app")

        tasks = asyncio.all_tasks(loop=loop)  # 5
        for task_ in tasks:
            task_.cancel()

        group = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()
