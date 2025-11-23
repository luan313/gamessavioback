from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from models.jogos_monitorados import JogosMonitorados
from schemas.jogos_monitorados import MonitoramentoCreate, MonitoramentoUpdate


async def create_monitoramento(db: AsyncSession, monitoramento: MonitoramentoCreate, user_id: UUID):
    db_monitoramento = JogosMonitorados(
        preco_alvo = monitoramento.preco_a_pagar,
        game_id=monitoramento.game_id, 
        user_id=user_id
    )

    db.add(db_monitoramento)
    await db.commit()
    await db.refresh(db_monitoramento)
    return db_monitoramento


async def get_monitored_games_for_user(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(JogosMonitorados)
        .where(JogosMonitorados.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_monitoramento_by_id(db: AsyncSession, monitoramento_id: UUID):
    result = await db.execute(select(JogosMonitorados).where(JogosMonitorados.id == monitoramento_id))
    return result.scalar_one_or_none()


async def update_monitoring(db: AsyncSession, monitoramento_id: UUID, monitoramento_update: MonitoramentoUpdate, user_id: UUID):
    db_monitoramento = await get_monitoramento_by_id(db, monitoramento_id)
    
    if not db_monitoramento:
        return None

    if db_monitoramento.user_id != user_id:
        return "unauthorized"

    if monitoramento_update.preco_a_pagar is not None:
        db_monitoramento.preco_alvo = monitoramento_update.preco_a_pagar
    
    await db.commit()
    await db.refresh(db_monitoramento)
    return db_monitoramento


async def delete_monitoramento(db: AsyncSession, monitoramento_id: UUID, user_id: UUID):
    db_monitoramento = await get_monitoramento_by_id(db, monitoramento_id)
    
    if not db_monitoramento:
        return None
    
    if db_monitoramento.user_id != user_id:
        return "unauthorized"

    await db.delete(db_monitoramento)
    await db.commit()
    return True