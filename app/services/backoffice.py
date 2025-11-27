from app.models.jogos_monitorados import JogosMonitorados
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BackOfficeService:
    @staticmethod
    async def get_all_games(db: AsyncSession):
        result = await db.execute(select(JogosMonitorados.id))
        game_ids = result.scalars().all()
        return game_ids