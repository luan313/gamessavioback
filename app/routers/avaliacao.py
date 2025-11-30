from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from fastapi_pagination import Page
from app.database.session import get_db
from app.core.security import get_current_user 
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoUpdate, AvaliacaoResponse, AvaliacaoBasicResponse, AvaliacaoDetailedResponse
from app.services import avaliacao as crud_avaliacao
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/avaliacoes")

@router.post(
    "/", 
    response_model=AvaliacaoResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar avaliação de jogo",
    description="Adiciona uma nova avaliação (nota e/ou comentário) de um usuário para um jogo específico. O usuário deve estar autenticado.",
    responses={
        201: {
            "description": "Avaliação criada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "game_id": "660e8400-e29b-41d4-a716-446655440001",
                        "user_id": "770e8400-e29b-41d4-a716-446655440002",
                        "nota": 4.5,
                        "comentario": "Jogo incrível! Jogabilidade perfeita.",
                        "created_at": "2024-11-24T18:07:00",
                        "updated_at": "2024-11-24T18:07:00"
                    }
                }
            }
        },
        401: {
            "description": "Usuário não autenticado",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Autenticação necessária", "details": None}
                }
            }
        },
        404: {
            "description": "Jogo não encontrado",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Jogo não encontrado", "details": None}
                }
            }
        }
    }
)
async def create_new_avaliacao(
    avaliacao: AvaliacaoCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> AvaliacaoResponse:
    """
        Cria uma nova avaliação para um jogo.
        
        Parâmetros:
        - **game_id**: UUID do jogo a ser avaliado
        - **nota**: Nota de 0 a 5 (com decimais, ex: 4.5)
        - **comentario**: Texto da avaliação (opcional)
        
        Retorna:
        - Dados da avaliação criada incluindo ID, nota, comentário e timestamps
        
        Regras:
        - Cada usuário pode criar apenas uma avaliação por jogo
        - A nota deve estar entre 0 e 5
        
        Requer autenticação: Sim (Bearer token)
    """
    return await crud_avaliacao.create_avaliacao(
        db = db, 
        avaliacao = avaliacao, 
        user_id = current_user.id
    )


@router.get(
    "/last-five-avaliations",
    response_model=list[AvaliacaoBasicResponse], 
    summary="Listar as últimas avaliações",
    description="Retorna as últimas avaliações feitas por usuários. Inclui notas, comentários e informações dos avaliadores.",
    responses={
        200: {
            "description": "Lista de avaliações retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "game_id": "660e8400-e29b-41d4-a716-446655440001",
                                "user_id": "770e8400-e29b-41d4-a716-446655440002",
                                "nota": 4.5,
                                "comentario": "Jogo incrível!",
                                "created_at": "2024-11-24T18:07:00",
                                "updated_at": "2024-11-24T18:07:00"
                            }
                        ],
                    }
                }
            }
        }
    }
)
async def read_last_five_avaliacoes(db: AsyncSession = Depends(get_db)) -> list[AvaliacaoBasicResponse]:
    return await crud_avaliacao.get_last_five_avaliacoes(db)


@router.get(
    "/game/{game_id}", 
    response_model=Page[AvaliacaoDetailedResponse], 
    summary="Listar avaliações de um jogo",
    description="Retorna todas as avaliações feitas para um jogo específico, com paginação. Inclui notas, comentários e informações dos avaliadores.",
    responses={
        200: {
            "description": "Lista de avaliações retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "game_id": "660e8400-e29b-41d4-a716-446655440001",
                                "user_id": "770e8400-e29b-41d4-a716-446655440002",
                                "nota": 4.5,
                                "comentario": "Jogo incrível!",
                                "created_at": "2024-11-24T18:07:00",
                                "updated_at": "2024-11-24T18:07:00"
                            }
                        ],
                        "total": 150,
                        "page": 1,
                        "size": 20
                    }
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
async def read_avaliacoes_game(
    game_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Page[AvaliacaoResponse]:
    """
        Retorna todas as avaliações de um jogo específico.
        
        Parâmetros:
        - **game_id**: UUID do jogo
        - **page**: Número da página (via query params)
        - **size**: Tamanho da página (via query params)
        
            Retorna:
            - Lista paginada de avaliações com notas, comentários e dados dos usuários
            - Informações de paginação (total, page, size)
            
            Não requer autenticação: Aberto ao público
    """
    query = crud_avaliacao.get_avaliacoes_by_game_id(game_id=game_id)
    return await paginate(db, query)  
    
    
@router.patch(
    "/{avaliacao_id}", 
    response_model=AvaliacaoResponse,
    summary="Editar minha avaliação",
    description="Atualiza uma avaliação existente (nota e/ou comentário). Apenas o autor da avaliação pode editá-la.",
    responses={
        200: {
            "description": "Avaliação atualizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "game_id": "660e8400-e29b-41d4-a716-446655440001",
                        "user_id": "770e8400-e29b-41d4-a716-446655440002",
                        "nota": 5.0,
                        "comentario": "Avaliação atualizada após DLC",
                        "created_at": "2024-11-24T18:07:00",
                        "updated_at": "2024-11-24T18:10:00"
                    }
                }
            }
        },
        403: {
            "description": "Não autorizado - tentativa de editar avaliação de outro usuário",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Não autorizado a editar esta avaliação", "details": None}
                }
            }
        },
        404: {
            "description": "Avaliação não encontrada",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Avaliação não encontrada", "details": None}
                }
            }
        }
    }
)
async def update_existing_avaliacao(
    avaliacao_id: UUID,
    avaliacao: AvaliacaoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> AvaliacaoResponse:
    """
        Atualiza uma avaliação existente.
        
        Parâmetros:
        - **avaliacao_id**: UUID da avaliação a ser atualizada
        - **nota**: Nova nota de 0 a 5 (opcional)
        - **comentario**: Novo texto da avaliação (opcional)
        
        Retorna:
        - Dados atualizados da avaliação com novo timestamp de updated_at
        
        Validações:
        - Apenas o autor da avaliação pode editá-la
        - Retorna 403 se tentar editar avaliação de outro usuário
        - Retorna 404 se a avaliação não existir
        
        Requer autenticação: Sim (Bearer token)
    """
    updated_avaliacao = await crud_avaliacao.update_avaliacao(
        db = db, 
        avaliacao_id = avaliacao_id, 
        avaliacao_update = avaliacao,
        user_id = current_user.id
    )
        
    return updated_avaliacao


@router.delete(
    "/{avaliacao_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar minha avaliação",
    description="Remove permanentemente uma avaliação do sistema. Apenas o autor pode deletar sua própria avaliação.",
    responses={
        204: {
            "description": "Avaliação deletada com sucesso (sem conteúdo)"
        },
        403: {
            "description": "Não autorizado - tentativa de deletar avaliação de outro usuário",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Não autorizado a deletar esta avaliação", "details": None}
                }
            }
        },
        404: {
            "description": "Avaliação não encontrada",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Avaliação não encontrada", "details": None}
                }
            }
        }
    }
)
async def delete_existing_avaliacao(
    avaliacao_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> None:
    """
        Remove uma avaliação permanentemente.
        
        Parâmetros:
        - **avaliacao_id**: UUID da avaliação a ser removida
        
        Comportamento:
        - Remove permanentemente a avaliação do banco de dados
        - A nota do usuário deixa de contar na média do jogo
        - Retorna status 204 (No Content) em caso de sucesso
        
        Validações:
        - Apenas o autor da avaliação pode deletá-la
        - Retorna 403 se tentar deletar avaliação de outro usuário
        - Retorna 404 se a avaliação não existir
        
        Requer autenticação: Sim (Bearer token)
    """
    await crud_avaliacao.delete_avaliacao(
        db = db, 
        avaliacao_id = avaliacao_id, 
        user_id = current_user.id
    )
    
    return None