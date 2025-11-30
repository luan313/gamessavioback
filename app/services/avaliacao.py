from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.avaliacao import Avaliacao 
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from sqlalchemy.orm import selectinload
from app.core.exceptions import ForbiddenException, NotFoundException

async def create_avaliacao(db: AsyncSession, avaliacao: AvaliacaoCreate, user_id: UUID) -> Avaliacao:
    db_avaliacao = Avaliacao(
        **avaliacao.model_dump(), 
        user_id=user_id 
    )
    db.add(db_avaliacao)
    await db.commit()
    await db.refresh(db_avaliacao)
    return db_avaliacao


def get_avaliacoes_by_game_id(game_id: UUID):
    return select(Avaliacao).options(selectinload(Avaliacao.user)).where(Avaliacao.game_id == game_id)


async def get_avaliacao_by_id(db: AsyncSession, avaliacao_id: UUID) -> Avaliacao | None: 
    result = await db.execute(select(Avaliacao).where(Avaliacao.id == avaliacao_id))
    return result.scalar_one_or_none()


async def update_avaliacao(db: AsyncSession, avaliacao_id: UUID, avaliacao_update: AvaliacaoUpdate, user_id: UUID) -> Avaliacao:
    db_avaliacao = await get_avaliacao_by_id(db, avaliacao_id)
    
    if not db_avaliacao:
        raise NotFoundException(message="Avaliação não encontrada")
    if db_avaliacao.user_id != user_id:
        raise ForbiddenException(message="Não autorizado a editar esta avaliação")

    update_data = avaliacao_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_avaliacao, key, value)

    await db.commit()
    await db.refresh(db_avaliacao)
    return db_avaliacao


async def delete_avaliacao(db: AsyncSession, avaliacao_id: UUID, user_id: UUID) -> bool:
    db_avaliacao = await get_avaliacao_by_id(db, avaliacao_id)
    
    if not db_avaliacao:
        raise NotFoundException(message="Avaliação não encontrada")
    if db_avaliacao.user_id != user_id:
        raise ForbiddenException(message="Não autorizado a deletar esta avaliação")

    await db.delete(db_avaliacao)
    await db.commit()
    return True


async def get_last_five_avaliacoes(db: AsyncSession) -> list[Avaliacao]:
    result = await db.execute(
        select(Avaliacao)
        .options(
            selectinload(Avaliacao.user),
            selectinload(Avaliacao.game)   
        )
        .order_by(Avaliacao.created_at.desc())
        .limit(5)
    )
    return result.scalars().all()