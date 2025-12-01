from app.models.jogos_monitorados import JogosMonitorados
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

class BackOfficeService:
    @staticmethod
    async def get_all_monitored_game_ids(db: AsyncSession) -> list[UUID]:
        result = await db.execute(select(JogosMonitorados.id))
        game_ids = result.scalars().all()
        return game_ids