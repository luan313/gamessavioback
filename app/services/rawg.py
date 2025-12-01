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

class RawgService:
    MARKERS = ["Español", "ESPAÑOL", "Français", "Deutsch", "Italiano", "Русский", "中文"]
    PAGE_SIZE = 40
    RATE_LIMIT_WAIT = 10
    
    @staticmethod
    def _clean_description(text: str) -> str:
        """
            Remove traduções extras que vêm concatenadas na descrição do RAWG.
            Ex: O texto vem em Inglês, seguido de 'Español' e o texto em espanhol.
            Cortamos tudo a partir da primeira ocorrência de outro idioma.
        """
        if not text:
            return ""
        
        for marker in RawgService.MARKERS:
            if f"\n{marker}" in text:
                text = text.split(f"\n{marker}")[0]
            elif f"\n\n{marker}" in text:
                text = text.split(f"\n\n{marker}")[0]
                
        return text.strip()


    @staticmethod
    async def get_description_from_rawg(game_data: dict, http_client: httpx.AsyncClient) -> str:
        """
            Busca a descrição do jogo no RAWG.
            
            Args:
                game_data (dict): Dados do jogo.
                http_client: Cliente HTTP para fazer requisições.
            
            Returns:
                str: Descrição do jogo.
        """
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
            
        return RawgService._clean_description(description)


    @staticmethod
    async def _process_genres(game: Game, genres_data: list[dict], db: AsyncSession) -> None:
        """
            Processa os gêneros do jogo.
            
            Args:
                game (Game): O jogo a ser processado.
                genres_data (list[dict]): Lista de gêneros do jogo.
                db (AsyncSession): Sessão assíncrona do banco de dados.
        """
        if not genres_data:
            return

        for genre_data in genres_data:
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


    @staticmethod
    async def _process_platforms(game: Game, platforms_data: list[dict], db: AsyncSession) -> None:
        """
            Processa as plataformas do jogo.
            
            Args:
                game (Game): O jogo a ser processado.
                platforms_data (list[dict]): Lista de plataformas do jogo.
                db (AsyncSession): Sessão assíncrona do banco de dados.
        """
        if not platforms_data:
            return

        for p_wrapper in platforms_data:
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


    @staticmethod
    async def _create_or_update_game(game_data: dict, db: AsyncSession, client) -> Game:
        """
            Cria ou atualiza um jogo no banco de dados.
            
            Args:
                game_data (dict): Dados do jogo.
                db (AsyncSession): Sessão assíncrona do banco de dados.
                client: Cliente HTTP para fazer requisições.
            
            Returns:
                Game: O jogo criado ou atualizado.
        """
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
        description = await RawgService.get_description_from_rawg(game_data, client)

        if not game:
            game = Game(
                nome=game_data.get("name"), 
                slug=game_data.get("slug"),
                rawg_id=rawg_id,
                metacritic=game_data.get("metacritic"),
                imagem_capa=game_data.get("background_image"),
                data_lancamento=release_date,
                descricao=description
            )
            db.add(game)
            await db.flush() 
        else:
            game.nome = game_data.get("name") 
            game.metacritic = game_data.get("metacritic")
            game.imagem_capa = game_data.get("background_image")
            game.updated_at = datetime.now()
            
        return game
            
            
    @staticmethod
    async def _import_game_from_response(game_data: dict, db: AsyncSession, client) -> Game:
        """
            Importa um jogo a partir de uma resposta do RAWG.
            
            Args:
                game_data (dict): Dados do jogo.
                db (AsyncSession): Sessão assíncrona do banco de dados.
                client: Cliente HTTP para fazer requisições.
            
            Returns:
                Game: O jogo importado.
        """
        logger.info(f"Importando: {game_data['name']}...")
        
        try:
            game = await RawgService._create_or_update_game(game_data, db, client)
            
            if "genres" in game_data:
                await RawgService._process_genres(game, game_data["genres"], db)
                    
            if "platforms" in game_data:            
                await RawgService._process_platforms(game, game_data["platforms"], db)
            
            await db.commit() 
            logger.info(f"Sucesso: {game.nome} salvo/atualizado!")
            return game
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Erro ao salvar {game_data.get('name')}: {e}")
            raise e
                  
        
    @staticmethod                 
    async def seed_games_by_amount(db: AsyncSession, amount=350) -> dict:
        """
            Carrega jogos do RAWG para o banco de dados.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                amount (int): Quantidade de jogos a serem carregados.
            
            Returns:
                dict: Dicionário contendo o total de jogos importados e o total de requisições.
        """
        total_importado = 0
        total_pages = math.ceil(amount / RawgService.PAGE_SIZE)
        logger.info(f"--- Iniciando Carga de {amount} jogos ({total_pages} requisições) ---")

        async with httpx.AsyncClient() as client:
            for page in range(1, total_pages + 1):
                logger.info(f"Requisitando página {page}/{total_pages}...")
                    
                params = {
                    "key": settings.RAWG_API_KEY,
                    "page_size": RawgService.PAGE_SIZE,
                    "ordering": "-added",
                    "page": page
                }
                    
                try:
                    resp = await client.get(settings.RAWG_BASE_URL, params=params)
                        
                    if resp.status_code == 429:
                        logger.warning(f"Rate Limit atingido! Esperando {RawgService.RATE_LIMIT_WAIT} segundos...")
                        await asyncio.sleep(RawgService.RATE_LIMIT_WAIT) 
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
                            await RawgService._import_game_from_response(game_json, db, client)
                            total_importado += 1
                                
                        except Exception as e_db:
                            logger.error(f"Skipping {game_json.get('name')}: {e_db}")
                                
                        await asyncio.sleep(0.1) 

                except Exception as e:
                    logger.error(f"Erro Geral: {e}")
        
        logger.info(f"--- Carga Finalizada! Total processado: {total_importado} jogos ---")
        return {"status": "success", "total": total_importado}