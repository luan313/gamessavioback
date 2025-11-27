
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.game import Game
from app.schemas.game import SearchGameResponse

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