import asyncio
import sys
import os

sys.path.append(os.getcwd())

from app.services.price_fetcher import update_game_price

if __name__ == "__main__":
    print("Iniciando script via terminal...")
    asyncio.run(update_game_price())