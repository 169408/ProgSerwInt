import asyncio

async def main() -> None:  # 1
    liczba = input("Wprowadź liczbę: ")
    while(type(liczba) != int):
        liczba = input("Wprowadź liczbę: ")
    a = 0
    b = 1
    counter = 0
    counter2 = 0
    while counter < liczba:
        if(counter == 0):
            print(0)
        elif(counter == 1):
            print(1)
        else:
            print(a + b)
            if(counter2 == 0):
                a += b
                counter2 += 1
            else:
                b += a
                counter2 -= 1

        counter += 1
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
