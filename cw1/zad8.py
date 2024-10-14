import asyncio

async def przetworz_plik(numer_pliku):
    print(f"Rozpoczynam wczytywanie pliku {numer_pliku}...")
    await asyncio.sleep(2)  # Symulacja czasu wczytywania
    print(f"Plik {numer_pliku} wczytany.")

    print(f"Rozpoczynam analizę pliku {numer_pliku}...")
    await asyncio.sleep(4)  # Symulacja czasu analizy
    print(f"Plik {numer_pliku} przeanalizowany.")

    print(f"Rozpoczynam zapis pliku {numer_pliku}...")
    await asyncio.sleep(1)  # Symulacja czasu zapisu
    print(f"Plik {numer_pliku} zapisany.")

async def main():
    # Tworzenie zadań dla pięciu plików
    zadania = []
    for i in range(1, 6):
        zadania.append(przetworz_plik(i))
    # Uruchomienie wszystkich zadań równocześnie
    await asyncio.gather(*zadania)

# Uruchomienie programu
if __name__ == "__main__":
    asyncio.run(main())