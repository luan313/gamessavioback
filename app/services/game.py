
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.game import Game

def get_top_hyped_games() -> list[Game]:
    return (
        select(Game)
        .order_by(Game.hype.desc())
    )