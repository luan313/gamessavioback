from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database.session import get_db
from app.schemas.categoria import CategoriaComJogos
from app.schemas.game import TopHypedGamesResponse
from app.services.categoria import CategoriaService
from sqlalchemy import select
from app.models.categoria import Categoria

router = APIRouter(prefix="/categoria")


@router.get(
    "/com-jogos",
    response_model=list[CategoriaComJogos],
    summary="Listar categorias com quantidade de jogos",
    description="Retorna todas as categorias com seus IDs, nomes e a quantidade de jogos em cada categoria.",
)
async def get_categorias_com_jogos(
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para obter todas as categorias com a quantidade de jogos.
    
    Retorna:
    - id: UUID da categoria
    - nome: Nome da categoria
    - quantidade_jogos: Número de jogos associados à categoria
    """
    categorias = await CategoriaService.get_categorias_com_quantidade_jogos(db)
    
    return [
        {
            "id": cat.id,
            "nome": cat.nome,
            "quantidade_jogos": cat.quantidade_jogos
        }
        for cat in categorias
    ]


@router.get(
    "/{categoria_id}/jogos",
    response_model=list[TopHypedGamesResponse],
    summary="Listar jogos de uma categoria",
    description="Retorna todos os jogos pertencentes a uma categoria específica, ordenados por nome.",
    responses={
        200: {
            "description": "Lista de jogos da categoria retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
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
                    ]
                }
            }
        },
        404: {
            "description": "Categoria não encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Categoria não encontrada"}
                }
            }
        }
    }
)
async def get_jogos_categoria(
    categoria_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
        Retorna todos os jogos de uma categoria específica.
        
        Parâmetros:
        - **categoria_id**: UUID da categoria
        
        Retorna:
        - Lista de jogos com todas as informações (nome, descrição, preço, hype, etc.)
        - Jogos ordenados alfabeticamente por nome
    """
    result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))
    categoria = result.scalar_one_or_none()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    jogos = await CategoriaService.get_jogos_por_categoria(db, categoria_id)
    
    return jogos
