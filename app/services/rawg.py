import math
import asyncio
import httpx
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_ 
from app.core.config import settings
from app.models.game import Game
from app.models.categoria import Categoria
from app.models.game_categoria import GameCategoria
from app.models.plataforma import Plataforma
from app.models.game_plataforma import GamePlataforma

import logging

logger = logging.getLogger(__name__)

class rawg_service:        
    
    @staticmethod
    def __clean_description(text: str) -> str:
        """
            Remove traduções extras que vêm concatenadas na descrição do RAWG.
            Ex: O texto vem em Inglês, seguido de 'Español' e o texto em espanhol.
            Cortamos tudo a partir da primeira ocorrência de outro idioma.
        """
        if not text:
            return ""
        
        markers = ["Español", "ESPAÑOL", "Français", "Deutsch", "Italiano", "Русский", "中文"]
        
        for marker in markers:
            if f"\n{marker}" in text:
                text = text.split(f"\n{marker}")[0]
            elif f"\n\n{marker}" in text:
                text = text.split(f"\n\n{marker}")[0]
                
        return text.strip()
    @staticmethod
    async def get_description_from_rawg(game_data: int, http_client) -> str:
        rawg_id = game_data.get("id")
        description = game_data.get("description_raw") or game_data.get("description")
        
        if not description and http_client and rawg_id:
            try:
                api_key = settings.RAWG_API_KEY
                response = await http_client.get(f"https://api.rawg.io/api/games/{rawg_id}?key={api_key}")
                
                if response.status_code == 200:
                    details = response.json()
                    description = details.get("description_raw")
            
            except Exception as e:
                logger.error(f"Erro ao buscar detalhes extras do jogo {rawg_id}: {e}")

        if not description:
            description = f"Released: {game_data.get('released')}"
            
        return rawg_service.__clean_description(description)

            
    @staticmethod
    async def __import_game_from_response(game_data: dict, db: AsyncSession, client) -> Game:
        logger.info(f"Importando: {game_data['name']}...")
        
        release_date = None
        if game_data.get("released"):
            try:
                release_date = datetime.strptime(game_data["released"], "%Y-%m-%d").date()
            except ValueError:
                pass

        rawg_id = game_data.get("id")
        query = select(Game).where(Game.rawg_id == rawg_id)
        result = await db.execute(query)
        game = result.scalar_one_or_none()
        description = await rawg_service.get_description_from_rawg(game_data, client)

        if not game:
            game = Game(
                nome=game_data.get("name"), 
                slug=game_data.get("slug"),
                rawg_id=rawg_id,
                metacritic=game_data.get("metacritic"),
                imagem_capa=game_data.get("background_image"),
                data_lancamento=release_date,
                descricao= description
            )
            db.add(game)
            await db.flush() 
        
        else:
            game.nome = game_data.get("name") 
            game.metacritic = game_data.get("metacritic")
            game.imagem_capa = game_data.get("background_image")
            game.updated_at = datetime.now()
        
        if "genres" in game_data:
            for genre_data in game_data["genres"]:
                cat_nome = genre_data["name"]
                cat_slug = genre_data.get("slug")
                
                result_cat = await db.execute(select(Categoria).where(Categoria.nome == cat_nome))
                categoria = result_cat.scalar_one_or_none()
                
                if not categoria:
                    categoria = Categoria(nome=cat_nome, slug=cat_slug)
                    db.add(categoria)
                    await db.flush()
                
                query_link = select(GameCategoria).where(
                    and_(
                        GameCategoria.game_id == game.id,
                        GameCategoria.categoria_id == categoria.id
                    )
                )
                result_link = await db.execute(query_link)
                link_existente = result_link.scalar_one_or_none()
                
                if not link_existente:
                    novo_link = GameCategoria(game_id=game.id, categoria_id=categoria.id)
                    db.add(novo_link)
                    
                    
        if "platforms" in game_data:            
            for p_wrapper in game_data["platforms"]:
                p_data = p_wrapper["platform"]
                plat_nome = p_data["name"]
                plat_slug = p_data.get("slug")
                
                result_plat = await db.execute(select(Plataforma).where(Plataforma.nome == plat_nome))
                plataforma = result_plat.scalar_one_or_none()
                
                if not plataforma:
                    plataforma = Plataforma(nome=plat_nome, slug=plat_slug)
                    db.add(plataforma)
                    await db.flush()
                    
                query_link_plat = select(GamePlataforma).where(
                    and_(
                        GamePlataforma.game_id == game.id,
                        GamePlataforma.plataforma_id == plataforma.id
                    )
                )
                result_link_plat = await db.execute(query_link_plat)
                link_plat_existente = result_link_plat.scalar_one_or_none()
                
                if not link_plat_existente:
                    novo_link_plat = GamePlataforma(game_id=game.id, plataforma_id=plataforma.id)
                    db.add(novo_link_plat)
        
        try:
            await db.commit() 
            logger.info(f"Sucesso: {game.nome} salvo/atualizado!")
            return game
        except Exception as e:
            await db.rollback()
            logger.error(f"Erro ao salvar {game_data.get('name')}: {e}")
            raise e
                  
        
    @staticmethod                 
    async def seed_games_by_amount(db: AsyncSession, amount=350) -> int:
        page_size = 40
        total_importado = 0
        total_pages = math.ceil(amount / page_size)
        logger.info(f"--- Iniciando Carga de {amount} jogos ({total_pages} requisições) ---")

        async with httpx.AsyncClient() as client:
            for page in range(1, total_pages + 1):
                logger.info(f"Requisitando página {page}/{total_pages}...")
                    
                params = {
                    "key": settings.RAWG_API_KEY,
                    "page_size": page_size,
                    "ordering": "-added",
                    "page": page
                }
                    
                try:
                    resp = await client.get(settings.RAWG_BASE_URL, params=params)
                        
                    if resp.status_code == 429:
                        logger.warning("Rate Limit atingido! Esperando 10 segundos...")
                        await asyncio.sleep(10) 
                        continue 
                            
                    if resp.status_code != 200:
                        logger.error(f"Erro API: {resp.status_code}")
                        break

                    data = resp.json()
                    results = data.get("results", [])
                        
                    if not results:
                        logger.info("Fim dos resultados na API.")
                        break

                    for game_json in results:
                        try:
                            await rawg_service.__import_game_from_response(game_json, db, client)
                            total_importado += 1
                                
                        except Exception as e_db:
                            logger.error(f"Skipping {game_json.get('name')}: {e_db}")
                                
                        await asyncio.sleep(0.1) 

                except Exception as e:
                    logger.error(f"Erro Geral: {e}")
        
        logger.info(f"--- Carga Finalizada! Total processado: {total_importado} jogos ---")
        return {"status": "success", "total": total_importado}