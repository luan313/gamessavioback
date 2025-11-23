from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_async
from app.database.session import get_db
from app.core.security import get_current_user 
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate, AvaliacaoResponse
from app.services import avaliacao_service as crud_avaliacao

router = APIRouter(prefix="/avaliacoes")

@router.post(
    "/", 
    response_model=AvaliacaoResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova avaliação",
    description="Adiciona uma avaliação (nota/texto) de um usuário para um jogo específico.",
    responses={
        401: {"description": "Usuário não autenticado"},
        404: {"description": "Jogo não encontrado"} 
    }
)
async def create_new_avaliacao(
    avaliacao: AvaliacaoCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await crud_avaliacao.create_avaliacao(db=db, avaliacao=avaliacao, user_id=current_user.id)


@router.get(
    "/game/{game_id}", 
    response_model=Page[AvaliacaoResponse], 
    summary="Listar avaliações de um jogo",
    description="Retorna as avaliações de um jogo específico de forma paginada.",
)
async def read_avaliacoes_game(
    game_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud_avaliacao.get_avaliacoes_by_game(db, game_id, skip, limit)


@router.patch(
    "/{avaliacao_id}", 
    response_model=AvaliacaoResponse,
    summary="Atualizar avaliação",
    description="Permite que o autor edite sua própria avaliação.",
    responses={
        403: {"description": "Não autorizado (Tentativa de editar avaliação de outro usuário)"},
        404: {"description": "Avaliação não encontrada"}
    }
)
async def update_existing_avaliacao(
    avaliacao_id: UUID,
    avaliacao: AvaliacaoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_avaliacao = await crud_avaliacao.update_avaliacao(
        db, avaliacao_id, avaliacao, current_user.id
    )
    
    if updated_avaliacao == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a editar esta avaliação")
    if not updated_avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        
    return updated_avaliacao

@router.delete(
    "/{avaliacao_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar avaliação",
    description="Remove uma avaliação. Apenas o autor pode deletar.",
    responses={
        403: {"description": "Não autorizado"},
        404: {"description": "Avaliação não encontrada"}
    }
)
async def delete_existing_avaliacao(
    avaliacao_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await crud_avaliacao.delete_avaliacao(db, avaliacao_id, current_user.id)
    
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a deletar esta avaliação")
    if not result:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    return None