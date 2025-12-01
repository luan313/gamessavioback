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
    TIMEOUT = 10.0
    BATCH_LIMIT = 200
    COUNTRY = "BR"
    API_SLEEP = 1.2

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(timeout=self.TIMEOUT)
        self.api_key = settings.ANY_DEAL_API_KEY
        self.base_url = settings.ANY_DEAL_BASE_URL

    async def close(self) -> None:
        """
            Fecha a sessão HTTP.
        """
        await self.client.aclose()


    async def get_game_id_from_itad(self, game_name: str) -> str | None:
        """
            Busca o ID ITAD de um jogo.
            
            Args:
                game_name (str): Nome do jogo.
            
            Returns:
                str | None: ID ITAD do jogo ou None se não encontrado.
        """
        await asyncio.sleep(self.API_SLEEP)  

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
        """
            Consulta os preços de todos os jogos no banco de dados.
            
            Args:
                itad_ids (list[str]): Lista de IDs ITAD dos jogos.
            
            Returns:
                dict[str, dict]: Dicionário com os preços de todos os jogos.
        """
        if not itad_ids:
            return {}

        try:
            response = await self.client.post(
                f"{self.base_url}/games/overview/v2",
                params={"key": self.api_key, "country": self.COUNTRY},
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

    async def _update_game_itad_ids(self, db: AsyncSession, games: list[Game]) -> None:
        """
            Atualiza os IDs ITAD dos jogos no banco de dados.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                games (list[Game]): Lista de jogos a serem atualizados.
        """
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


    async def _fetch_all_prices(self, ids: list[str]) -> dict:
        """
            Consulta os preços de todos os jogos no banco de dados.
            
            Args:
                ids (list[str]): Lista de IDs dos jogos.
            
            Returns:
                dict: Dicionário com os preços de todos os jogos.
        """
        logger.info(f"Consultando preços de {len(ids)} jogos em lote...")
        all_prices = {} 

        for i in range(0, len(ids), self.BATCH_LIMIT):
            chunk = ids[i : i + self.BATCH_LIMIT]
            logger.info(f"Processando lote {i} a {i + len(chunk)}...")
            
            try:
                batch_result = await self.get_prices_batch(chunk)
                
                if batch_result:
                    all_prices.update(batch_result)
                    
            except Exception as e:
                logger.error(f"Erro ao processar lote começando em {i}: {e}")
        
        return all_prices


    def _normalize_prices(self, ids: list[str], prices: dict) -> dict:
        """
            Normaliza os preços dos jogos.
            
            Args:
                ids (list[str]): Lista de IDs dos jogos.
                prices (dict): Dicionário com os preços.
            
            Returns:
                dict: Dicionário com os preços normalizados.
        """
        normalized_prices = {}
        for original_id in ids:
            for returned_id, info in prices.items():
                if returned_id.startswith(original_id):
                    normalized_prices[original_id] = info
                    break
        return normalized_prices


    async def _update_games_with_prices(self, db: AsyncSession, games: list[Game], normalized_prices: dict) -> None:
        """
            Atualiza os preços dos jogos no banco de dados com os preços do ITAD.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                games (list[Game]): Lista de jogos a serem atualizados.
                normalized_prices (dict): Dicionário com os preços normalizados.
        """
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


    async def sync_all_games_prices(self, db: AsyncSession) -> dict:
        """
            Sincroniza os preços de todos os jogos no banco de dados com os preços do ITAD.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
            
            Returns:
                dict: Dicionário com o status do sync.
        """
        logger.info("--- Iniciando Sync ITAD ---")

        result = await db.execute(select(Game))
        games = result.scalars().all()

        await self._update_game_itad_ids(db, games)

        ids = [g.isthereanydeal_id for g in games if g.isthereanydeal_id]

        if not ids:
            logger.warning("Nenhum jogo com ID ITAD válido.")
            return {"status": "no_ids"}

        all_prices = await self._fetch_all_prices(ids)
        normalized_prices = self._normalize_prices(ids, all_prices)
        
        await self._update_games_with_prices(db, games, normalized_prices)

        logger.info("--- Sync Finalizado com Sucesso ---")
        return {"status": "finished"}