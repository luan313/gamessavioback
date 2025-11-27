from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from app.models.jogos_monitorados import JogosMonitorados
from app.schemas.jogos_monitorados import MonitoramentoCreate, MonitoramentoUpdate
from sqlalchemy.orm import selectinload

class MonitoramentoService:
    @staticmethod
    async def create_monitoramento(db: AsyncSession, monitoramento: MonitoramentoCreate, user_id: UUID) -> JogosMonitorados:
        db_monitoramento = JogosMonitorados(
            preco_alvo = monitoramento.preco_alvo,
            game_id=monitoramento.game_id, 
            user_id=user_id
        )

        db.add(db_monitoramento)
        await db.commit()
        
        query = (
            select(JogosMonitorados)
            .options(selectinload(JogosMonitorados.game))  
            .where(JogosMonitorados.id == db_monitoramento.id)
        )
        
        result = await db.execute(query)
        monitoramento_criado = result.scalars().first()
        
        return monitoramento_criado

    @staticmethod
    async def get_monitored_games_for_user(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> list[JogosMonitorados]:
        result = await db.execute(
            select(JogosMonitorados)
            .options(selectinload(JogosMonitorados.game))
            .where(JogosMonitorados.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


    @staticmethod
    async def get_monitoramento_by_id(db: AsyncSession, monitoramento_id: UUID) -> JogosMonitorados | None:
        result = await db.execute(select(JogosMonitorados).where(JogosMonitorados.id == monitoramento_id))
        return result.scalar_one_or_none()


    @staticmethod
    async def update_monitoring(db: AsyncSession, monitoramento_id: UUID, monitoramento_update: MonitoramentoUpdate, user_id: UUID) -> JogosMonitorados | None:
        db_monitoramento = await MonitoramentoService.get_monitoramento_by_id(db, monitoramento_id)
        
        if not db_monitoramento:
            return None

        if db_monitoramento.user_id != user_id:
            return "unauthorized"

        if monitoramento_update.preco_a_pagar is not None:
            db_monitoramento.preco_alvo = monitoramento_update.preco_a_pagar
        
        await db.commit()
        await db.refresh(db_monitoramento)
        return db_monitoramento


    @staticmethod
    async def delete_monitoramento(db: AsyncSession, monitoramento_id: UUID, user_id: UUID) -> bool | None:
        db_monitoramento = await MonitoramentoService.get_monitoramento_by_id(db, monitoramento_id)
        
        if not db_monitoramento:
            return None
        
        if db_monitoramento.user_id != user_id:
            return "unauthorized"

        await db.delete(db_monitoramento)
        await db.commit()
        return True