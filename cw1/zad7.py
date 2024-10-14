import asyncio
import random

async def krojenie() -> None:
    await asyncio.sleep(2)
    print("pokrojone")

async def gotowanie() -> None:
    await asyncio.sleep(6)
    print("ugotowane")

async def smazenie() -> None:
    await asyncio.sleep(3)
    print("posmazono")

async def main() -> None:
    danie = input("Wprowadź jedno z dań [mięso - 1, herbata - 2, makaron z salatem - 3]: ")
    if (danie == 1):
        await asyncio.gather(krojenie(), smazenie())
        print("smacznego")
    if (danie == 2):
        await asyncio.gather(gotowanie())
        print("smacznego")

if __name__ == "__main__":
    asyncio.run(main())
