
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.game import Game

def get_top_hyped_games(db: AsyncSession, limit: int = 20):
    query = (
        select(Game)
        .order_by(Game.hype.desc())
        .limit(limit)
    )
    return query
