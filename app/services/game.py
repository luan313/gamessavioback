
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.game import SearchGameResponse
from uuid import UUID
from sqlalchemy.orm import selectinload
from app.models.game import Game
from app.models.game_categoria import GameCategoria
from app.models.game_plataforma import GamePlataforma
from app.core.exceptions import NotFoundException

def get_top_hyped_games() -> list[Game]:
    return (
        select(Game)
        .order_by(Game.hype.desc())
    )


def search_games_by_name(name: str) -> list[SearchGameResponse]:
    return (
        select(Game)
        .where(Game.nome.ilike(f"%{name}%"))
    )


def get_game_by_id(id: UUID) -> Game:
    stmt = (
        select(Game)
        .options(
            selectinload(Game.categorias).joinedload(GameCategoria.categoria),  
            selectinload(Game.plataformas).joinedload(GamePlataforma.plataforma),
        )
        .where(Game.id == id)
    )
    return stmt
    