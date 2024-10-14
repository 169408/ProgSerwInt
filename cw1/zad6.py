import asyncio
import random

async def fetch(delay: int) -> None:
    await asyncio.sleep(delay)
    print(random.randint(1000, 1000000))

async  def main() -> None:
    await asyncio.gather(fetch(2), fetch(1), fetch(3))
    #await fetch(2)

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())