
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.game import SearchGameResponse
from uuid import UUID
from sqlalchemy.orm import selectinload
from app.models.game import Game
from app.models.game_categoria import GameCategoria
from app.models.game_plataforma import GamePlataforma
from app.core.exceptions import NotFoundException

def get_top_hyped_games() -> Select:
    """
        Retorna uma query SQLAlchemy para listar jogos ordenados por hype.
        Projetado para ser usado com fastapi-pagination.
    """
    return (
        select(Game)
        .order_by(Game.hype.desc())
    )


def search_games_by_name(name: str) -> Select:
    """
        Retorna uma query SQLAlchemy para buscar jogos por nome.
        Projetado para ser usado com fastapi-pagination.
    """
    return (
        select(Game)
        .where(Game.nome.ilike(f"%{name}%"))
    )


def get_game_by_id(id: UUID) -> Select:
    """
        Retorna uma query SQLAlchemy para buscar um jogo por ID com relacionamentos carregados.
    """
    stmt = (
        select(Game)
        .options(
            selectinload(Game.categorias).joinedload(GameCategoria.categoria),  
            selectinload(Game.plataformas).joinedload(GamePlataforma.plataforma),
        )
        .where(Game.id == id)
    )
    return stmt

def get_all_games() -> Select:
    """
        Retorna uma query SQLAlchemy para listar todos os jogos.
        Projetado para ser usado com fastapi-pagination.
    """
    return select(Game)