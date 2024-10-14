import asyncio

async def maszynaA(time):
    ile = time // 2
    for i in range(ile):
        print("Maszyna Asasin zaczyna dzialanie #", i)
        await asyncio.sleep(2)
        print("Maszyna Asasin skonczyla dzialanie")

async def maszynaB(time):
    ile = time // 3
    for i in range(ile):
        print("Maszyna Baxia zaczyna dzialanie #", i)
        await asyncio.sleep(3)
        print("Maszyna Baxia skonczyla dzialanie")

async def maszynaC(time):
    ile = time // 5
    for i in range(ile):
        print("Maszyna Cerberus zaczyna dzialanie #", i)
        await asyncio.sleep(5)
        print("Maszyna Cerberus skonczyla dzialanie")

async def main():
    zadania = [maszynaA(15), maszynaB(15), maszynaC(15)]

    await asyncio.gather(*zadania)
    
if __name__ == "__main__":
    asyncio.run(main())