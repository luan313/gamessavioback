import asyncio
import httpx
import logging
from sqlalchemy import select, update
from app.database.session import AsyncSessionLocal
from app.models import Game
from app.core.config import settings

logger = logging.getLogger(__name__)

def chunked_list(list, size=200):
    for i in range(0, len(list), size):
        yield list[i:i + size]


async def update_game_price():
    """
        Atualiza os preços dos jogos no banco de dados.
    """
    logger.info("🚀 Iniciando atualização de preços...")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Game.id, Game.isthereanydeal_id))

        db_rows = result.all()
        
        games_map = {row.isthereanydeal_id: row.id for row in db_rows if row.isthereanydeal_id}

        id_itad = list(games_map.keys())

        logger.info(f"🎮 Jogos para atualizar: {len(id_itad)}")
        
        url = f"{settings.ANY_DEAL_BASE_URL}/games/prices/v3?key={settings.ANY_DEAL_API_KEY}&country=BR"

        async with httpx.AsyncClient() as client:
            for chunk_id_itad in chunked_list(id_itad, 200):
                try:
                    response = await client.post(url, json=chunk_id_itad)

                    deals = response.json()

                    deals_list = []

                    for deal in deals:
                        api_id = deal.get("id")

                        offers = deal.get("deals", [])

                        price = None

                        if isinstance(offers, list) and len(offers) > 0:
                            valid_prices = []

                            for offer in offers:
                                amount = offer.get("price", {}).get("amount")

                                if amount is not None:
                                    valid_prices.append(amount)

                        if valid_prices:
                            price = min(valid_prices)

                        if api_id in games_map and price is not None:
                            db_id = games_map[api_id]
                            
                            deals_list.append({
                                "id": db_id,
                                "last_price": price
                            })
            
                    if deals_list:
                        await session.execute(update(Game), deals_list)
                        await session.commit()
                        logger.info(f"Lote atualizado: {len(deals_list)} jogos.")

                except Exception as e:
                    logger.error(f"Erro no lote: {e}")
