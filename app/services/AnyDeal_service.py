import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.game import Game
from datetime import datetime 
import asyncio
from app.database.session import AsyncSessionLocal

class AnyDealService:
    @staticmethod
    async def get_game_id_from_itad(game_name: str) -> str | None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.ANY_DEAL_BASE_URL}/games/search/v1",
                    params={
                        "key": settings.ANY_DEAL_API_KEY,
                        "title": game_name,
                        "limit": 1
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                if data and len(data) > 0:
                    return data[0].get("id") 
                
            except Exception as e:
                print(f"Erro ao buscar ID ITAD ({game_name}): {e}")
                return None
        return None

    @staticmethod
    async def get_current_price(itad_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post( 
                    f"{settings.ANY_DEAL_BASE_URL}/games/overview/v2",
                    params={
                        "key": settings.ANY_DEAL_API_KEY,
                        "country": "BR"
                    },
                    json=[itad_id],
                    timeout=10.0
                )
                
                result_data = {
                    "price": 0.0,
                    "url": None,
                    "store": None
                }

                if response.status_code != 200:
                    return result_data
                
                data = response.json()
                prices_list = data.get("prices", [])
                
                game_entry = None
                for item in prices_list:
                    if item.get("id") == itad_id:
                        game_entry = item
                        break
                
                if not game_entry and prices_list:
                    game_entry = prices_list[0]
                
                if not game_entry:
                    return result_data

                current_obj = game_entry.get("current", {})
                
                price_obj = current_obj.get("price")
                if price_obj and isinstance(price_obj, dict):
                    amount = price_obj.get("amount")
                    if amount is not None:
                        result_data["price"] = float(amount)

                result_data["url"] = current_obj.get("url")

                shop_obj = current_obj.get("shop")
                if shop_obj and isinstance(shop_obj, dict):
                    result_data["store"] = shop_obj.get("name")

                return result_data

            except Exception as e:
                print(f"Erro ao buscar preço ITAD ({itad_id}): {e}")
                return {"price": 0.0, "url": None, "store": None}


    @staticmethod
    async def _process_game_task(game_id: str, semaphore: asyncio.Semaphore):
        async with semaphore: 
            async with AsyncSessionLocal() as session:
                try:
                    result = await session.execute(select(Game).where(Game.id == game_id))
                    game = result.scalar_one_or_none()
                    if not game: return


                    await asyncio.sleep(0.2) 
                    print(f"[{game.nome}] Buscando ofertas...")
                    
                    deal_data = await AnyDealService.get_current_price(game.isthereanydeal_id)
                    
                    game.last_price = deal_data["price"]
                    game.deal_url = deal_data["url"]     
                    game.store_name = deal_data["store"] 
                    game.updated_at = datetime.now() 
                    
                    session.add(game)
                    await session.commit()
                    
                    if deal_data["price"] > 0:
                        print(f"[{game.nome}] R$ {deal_data['price']} na {deal_data['store']}")
                    else:
                        print(f"[{game.nome}] Sem oferta ativa.")
                    
                except Exception as e:
                    print(f"Erro processando jogo {game_id}: {e}")

 
    @staticmethod
    async def sync_all_games_prices(db: AsyncSession):
        print("--- Iniciando Sync ---")
        result = await db.execute(select(Game.id))
        game_ids = result.scalars().all()
        
        print(f"Total na fila: {len(game_ids)}")

        semaphore = asyncio.Semaphore(4)

        tasks = [AnyDealService._process_game_task(str(gid), semaphore) for gid in game_ids]
        
        await asyncio.gather(*tasks)
        
        print("--- Sync Finalizado ---")
        return {"status": "finished"}