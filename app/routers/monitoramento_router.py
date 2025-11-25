from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database.session import get_db
from app.core.security import get_current_user
from app.schemas.jogos_monitorados import MonitoramentoCreate, MonitoramentoUpdate, MonitoramentoResponse 
from app.services import monitoramento_service as crud_monitoramento

router = APIRouter(prefix="/monitoramentos")

@router.post(
    "/", 
    response_model=MonitoramentoResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar alerta de preço para um jogo",
    description="Adiciona um jogo à lista de monitoramento do usuário autenticado. Quando o preço do jogo cair abaixo do valor especificado, o usuário pode ser notificado.",
    responses={
        201: {
            "description": "Monitoramento criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "game_id": "660e8400-e29b-41d4-a716-446655440001",
                        "user_id": "770e8400-e29b-41d4-a716-446655440002",
                        "preco_alvo": 29.99,
                        "ativo": True,
                        "created_at": "2024-11-24T18:05:00"
                    }
                }
            }
        },
        409: {
            "description": "Jogo já está sendo monitorado pelo usuário",
            "content": {
                "application/json": {
                    "example": {"detail": "Este jogo já está na sua lista de monitoramento"}
                }
            }
        },
        404: {
            "description": "Jogo não encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Jogo não encontrado"}
                }
            }
        }
    }
)
async def create_new_monitoramento(
    monitoramento: MonitoramentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
        Cria um novo monitoramento de preço para um jogo.
        
        Parâmetros:
        - **game_id**: UUID do jogo a ser monitorado
        - **preco_alvo**: Preço desejado para receber alerta (opcional)
        - **ativo**: Se o monitoramento está ativo (opcional, padrão: true)
        
        Retorna:
        - Dados do monitoramento criado incluindo ID, game_id, user_id e data de criação
        
        Requer autenticação: Sim (Bearer token)
    """
    return await crud_monitoramento.create_monitoramento(db=db, monitoramento=monitoramento, user_id=current_user.id)


@router.get(
    "/", 
    response_model=list[MonitoramentoResponse], 
    summary="Listar meus monitoramentos de preço",
    description="Retorna todos os jogos que o usuário autenticado está monitorando, com informações sobre preço alvo e status do alerta.",
    responses={
        200: {
            "description": "Lista de monitoramentos retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "game_id": "660e8400-e29b-41d4-a716-446655440001",
                            "user_id": "770e8400-e29b-41d4-a716-446655440002",
                            "preco_alvo": 29.99,
                            "ativo": True,
                            "created_at": "2024-11-24T18:05:00"
                        }
                    ]
                }
            }
        }
    }
)
async def read_monitoramentos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
        Lista todos os jogos monitorados pelo usuário atual.
        
        Parâmetros:
        - **skip**: Número de registros a pular (paginação, padrão: 0)
        - **limit**: Número máximo de registros a retornar (padrão: 100)
        
        Retorna:
        - Lista de monitoramentos com game_id, preco_alvo, status ativo, etc.
        - Apenas os monitoramentos do usuário autenticado são retornados
        
        Requer autenticação: Sim (Bearer token)
    """
    return await crud_monitoramento.get_monitored_games_for_user(db, current_user.id, skip, limit)


@router.patch(
    "/{monitoramento_id}", 
    response_model=MonitoramentoResponse,
    summary="Atualizar configurações de alerta",
    description="Atualiza as condições de um monitoramento existente, como preço alvo ou status ativo/inativo. Apenas o dono do monitoramento pode editá-lo.",
    responses={
        200: {
            "description": "Monitoramento atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "game_id": "660e8400-e29b-41d4-a716-446655440001",
                        "user_id": "770e8400-e29b-41d4-a716-446655440002",
                        "preco_alvo": 19.99,
                        "ativo": True,
                        "created_at": "2024-11-24T18:05:00"
                    }
                }
            }
        },
        403: {
            "description": "Não autorizado - este monitoramento pertence a outro usuário",
            "content": {
                "application/json": {
                    "example": {"detail": "Não autorizado a editar este monitoramento"}
                }
            }
        },
        404: {
            "description": "Monitoramento não encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Monitoramento não encontrado"}
                }
            }
        }
    }
)
async def update_existing_monitoramento(
    monitoramento_id: UUID,
    monitoramento: MonitoramentoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
        Atualiza um monitoramento de preço existente.
        
        Parâmetros:
        - **monitoramento_id**: UUID do monitoramento a ser atualizado
        - **preco_alvo**: Novo preço alvo (opcional)
        - **ativo**: Ativar/desativar o monitoramento (opcional)
        
        Retorna:
        - Dados atualizados do monitoramento
        
        Validações:
        - Apenas o usuário que criou o monitoramento pode atualizá-lo
        - Retorna 403 se tentar editar monitoramento de outro usuário
        - Retorna 404 se o monitoramento não existir
        
        Requer autenticação: Sim (Bearer token)
    """
    updated_monitoramento = await crud_monitoramento.update_monitoring(
        db, monitoramento_id, monitoramento, current_user.id
    )

    if updated_monitoramento == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a editar este monitoramento")
    
    if not updated_monitoramento:
        raise HTTPException(status_code=404, detail="Monitoramento não encontrado")
        
    return updated_monitoramento


@router.delete(
    "/{monitoramento_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover monitoramento de preço",
    description="Remove um jogo da lista de monitoramento do usuário. O jogo deixará de ser monitorado e não receberá mais alertas de preço.",
    responses={
        204: {
            "description": "Monitoramento removido com sucesso (sem conteúdo)"
        },
        403: {
            "description": "Não autorizado - este monitoramento pertence a outro usuário",
            "content": {
                "application/json": {
                    "example": {"detail": "Não autorizado a remover este monitoramento"}
                }
            }
        },
        404: {
            "description": "Monitoramento não encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Monitoramento não encontrado"}
                }
            }
        }
    }
)
async def delete_existing_monitoramento(
    monitoramento_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
        Remove um monitoramento de preço.
        
        Parâmetros:
        - **monitoramento_id**: UUID do monitoramento a ser removido
        
        Comportamento:
        - Remove permanentemente o monitoramento do banco de dados
        - O jogo deixa de ser monitorado e não haverá mais alertas
        - Retorna status 204 (No Content) em caso de sucesso
        
        Validações:
        - Apenas o usuário que criou o monitoramento pode removê-lo
        - Retorna 403 se tentar remover monitoramento de outro usuário
        - Retorna 404 se o monitoramento não existir
        
        Requer autenticação: Sim (Bearer token)
    """
    result = await crud_monitoramento.delete_monitoramento(db, monitoramento_id, current_user.id)

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Não autorizado a remover este monitoramento")
    
    if not result:
        raise HTTPException(status_code=404, detail="Monitoramento não encontrado")
    
    return None