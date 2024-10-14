import asyncio

async def gloo() -> None:
    await asyncio.sleep(3)
    print("Hello")

async def gloo2() -> None:
    await asyncio.sleep(1)
    print("Hello2")

async def main() -> None:
    await gloo()
    await gloo2()


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())