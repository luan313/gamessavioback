from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.avaliacao import Avaliacao 
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from sqlalchemy.orm import selectinload

async def create_avaliacao(db: AsyncSession, avaliacao: AvaliacaoCreate, user_id: UUID):
    db_avaliacao = Avaliacao(
        **avaliacao.model_dump(), 
        user_id=user_id 
    )
    db.add(db_avaliacao)
    await db.commit()
    await db.refresh(db_avaliacao)
    return db_avaliacao


async def get_avaliacoes_by_game(db: AsyncSession, game_id: UUID, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Avaliacao)
        .where(Avaliacao.game_id == game_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_avaliacao_by_id(db: AsyncSession, avaliacao_id: UUID):
    result = await db.execute(select(Avaliacao).where(Avaliacao.id == avaliacao_id))
    return result.scalar_one_or_none()


async def update_avaliacao(db: AsyncSession, avaliacao_id: UUID, avaliacao_update: AvaliacaoUpdate, user_id: UUID):
    db_avaliacao = await get_avaliacao_by_id(db, avaliacao_id)
    
    if not db_avaliacao:
        return None
    if db_avaliacao.user_id != user_id:
        return "unauthorized"

    update_data = avaliacao_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_avaliacao, key, value)

    await db.commit()
    await db.refresh(db_avaliacao)
    return db_avaliacao


async def delete_avaliacao(db: AsyncSession, avaliacao_id: UUID, user_id: UUID):
    db_avaliacao = await get_avaliacao_by_id(db, avaliacao_id)
    
    if not db_avaliacao:
        return None
    if db_avaliacao.user_id != user_id:
        return "unauthorized"

    await db.delete(db_avaliacao)
    await db.commit()
    return True

async def get_last_five_avaliacoes(db: AsyncSession):
    result = await db.execute(
        select(Avaliacao)
        .options(selectinload(Avaliacao.user))
        .order_by(Avaliacao.created_at.desc())
        .limit(5)
    )
    return result.scalars().all()