from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database.session import get_db
from app.schemas.categoria import CategoriaComJogos
from app.schemas.game import TopHypedGamesResponse
from app.services.categoria import CategoriaService
from sqlalchemy import select
from app.models.categoria import Categoria
from fastapi_cache.decorator import cache
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params, Page

router = APIRouter(prefix="/categoria")


@router.get(
    "/com-jogos",
    response_model=list[CategoriaComJogos],
    summary="Listar categorias com quantidade de jogos",
    description="Retorna todas as categorias com seus IDs, nomes e a quantidade de jogos em cada categoria.",
    responses={
        200: {
            "description": "Lista de categorias retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "nome": "RPG",
                            "quantidade_jogos": 15
                        },
                        {
                            "id": "660e8400-e29b-41d4-a716-446655440001",
                            "nome": "Ação",
                            "quantidade_jogos": 23
                        }
                    ]
                }
            }
        }
    }
)
@cache(expire=3600)
async def get_categorias_com_jogos(
    db: AsyncSession = Depends(get_db),
    _ = Depends(RateLimiter(times=60, seconds=60))
):
    """
    Endpoint para obter todas as categorias com a quantidade de jogos.
    
    Retorna:
    - id: UUID da categoria
    - nome: Nome da categoria
    - quantidade_jogos: Número de jogos associados à categoria
    """
    categorias = await CategoriaService.get_categorias_com_quantidade_jogos(db)
    return categorias


@router.get(
    "/{categoria_id}/jogos",
    response_model=Page[TopHypedGamesResponse],
    summary="Listar jogos de uma categoria",
    description="Retorna todos os jogos pertencentes a uma categoria específica, ordenados por nome.",
    responses={
        200: {
            "description": "Lista de jogos da categoria retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "nome": "The Witcher 3",
                                "slug": "the-witcher-3",
                                "descricao": "Um RPG de ação...",
                                "imagem_capa": "https://...",
                                "data_lancamento": "2015-05-19",
                                "metacritic": 92,
                                "nota_media": 4.5,
                                "last_price": 29.99,
                                "deal_url": "https://...",
                                "store_name": "Steam",
                                "hype": 8500,
                                "updated_at": "2024-11-24T17:57:00"
                            }
                        ],
                        "total": 100,
                        "page": 1,
                        "size": 20
                    }
                }
            }
        },
        404: {
            "description": "Categoria não encontrada",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Categoria não encontrada", "details": None}
                }
            }
        }
    }
)
@cache(expire=3600)
async def get_jogos_categoria(
    categoria_id: UUID,
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db),
    _ = Depends(RateLimiter(times=60, seconds=60))
):
    """
        Retorna todos os jogos de uma categoria específica.
        
        Parâmetros:
        - **categoria_id**: UUID da categoria
        
        Retorna:
        - Lista de jogos com todas as informações (nome, descrição, preço, hype, etc.)
        - Jogos ordenados alfabeticamente por nome
    """
    query = await CategoriaService.get_jogos_por_categoria(db, categoria_id)

    return await paginate(
        db, 
        query, 
        params
    )
