import httpx
import asyncio
import logging
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.game import Game
from app.database.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

class AnyDealService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
        self.api_key = settings.ANY_DEAL_API_KEY
        self.base_url = settings.ANY_DEAL_BASE_URL

    async def close(self):
        await self.client.aclose()


    async def get_game_id_from_itad(self, game_name: str) -> str | None:
        await asyncio.sleep(1.2)  

        try:
            response = await self.client.get(
                f"{self.base_url}/games/search/v1",
                params={
                    "key": self.api_key,
                    "title": game_name,
                    "limit": 1
                }
            )
            response.raise_for_status()
            data = response.json()
            if data and len(data) > 0:
                return data[0].get("id")

        except Exception as e:
            logger.error(f"Erro ao buscar ID ITAD para '{game_name}': {e}")

        return None


    async def get_prices_batch(self, itad_ids: list[str]) -> dict[str, dict]:
        if not itad_ids:
            return {}

        try:
            response = await self.client.post(
                f"{self.base_url}/games/overview/v2",
                params={"key": self.api_key, "country": "BR"},
                json=itad_ids  
            )

            if response.status_code != 200:
                logger.error(f"Erro overview batch: {response.text}")
                return {}

            data = response.json()
            prices_raw = data.get("prices", [])
            prices = {}

            for item in prices_raw:
                itad_id = item.get("id")
                current = item.get("current", {})

                price = current.get("price", {}).get("amount") or 0
                url = current.get("url")
                store = current.get("shop", {}).get("name")

                prices[itad_id] = {
                    "price": float(price),
                    "url": url,
                    "store": store
                }

            return prices

        except Exception as e:
            logger.error(f"Erro no batch de preços: {e}")
            return {}


    async def sync_all_games_prices(self, db: AsyncSession) -> dict:
        logger.info("--- Iniciando Sync ITAD ---")

        result = await db.execute(select(Game))
        games = result.scalars().all()

        for game in games:
            if not game.isthereanydeal_id:
                logger.info(f"Buscando ID ITAD para: {game.nome}")
                itad_id = await self.get_game_id_from_itad(game.nome)

                if not itad_id:
                    logger.warning(f"Não encontrado no ITAD: {game.nome}")
                    continue

                game.isthereanydeal_id = itad_id
                db.add(game)
                await db.commit()

        ids = [g.isthereanydeal_id for g in games if g.isthereanydeal_id]

        if not ids:
            logger.warning("Nenhum jogo com ID ITAD válido.")
            return {"status": "no_ids"}

        logger.info(f"Consultando preços de {len(ids)} jogos em lote...")
        BATCH_LIMIT = 200
        all_prices = {} 

        for i in range(0, len(ids), BATCH_LIMIT):
            chunk = ids[i : i + BATCH_LIMIT]
            logger.info(f"Processando lote {i} a {i + len(chunk)}...")
            
            try:
                batch_result = await self.get_prices_batch(chunk)
                
                if batch_result:
                    all_prices.update(batch_result)
                    
            except Exception as e:
                logger.error(f"Erro ao processar lote começando em {i}: {e}")

        prices = all_prices

        normalized_prices = {}
        for original_id in ids:
            for returned_id, info in prices.items():
                if returned_id.startswith(original_id):
                    normalized_prices[original_id] = info
                    break

        for game in games:
            itad_id = game.isthereanydeal_id
            if not itad_id:
                continue

            info = normalized_prices.get(itad_id)
            if not info:
                continue

            game.last_price = info["price"]
            game.deal_url = info["url"]
            game.store_name = info["store"]
            game.updated_at = datetime.now()

            db.add(game)

        await db.commit()

        logger.info("--- Sync Finalizado com Sucesso ---")
        return {"status": "finished"}