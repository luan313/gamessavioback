from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.game import TopHypedGamesResponse
from app.services import game as game_service
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_async
from fastapi_pagination import Page, Params
from fastapi import Query

router = APIRouter(prefix="/game")

@router.get(
    "/hyped-games", 
    response_model=Page[TopHypedGamesResponse],
    summary="Listar jogos mais populares",
    description="Retorna uma lista paginada de jogos ordenados pelo Hype Score (popularidade). O Hype Score é calculado com base em múltiplos fatores como interesse da comunidade, avaliações e engajamento.",
    responses={
        200: {
            "description": "Lista de jogos populares retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "nome": "Elden Ring",
                                "slug": "elden-ring",
                                "descricao": "Um RPG de ação em mundo aberto...",
                                "imagem_capa": "https://media.rawg.io/media/...",
                                "data_lancamento": "2022-02-25",
                                "metacritic": 96,
                                "nota_media": 4.8,
                                "last_price": 59.99,
                                "deal_url": "https://isthereanydeal.com/...",
                                "store_name": "Steam",
                                "hype": 15000,
                                "updated_at": "2024-11-24T18:00:00"
                            }
                        ],
                        "total": 100,
                        "page": 1,
                        "size": 20
                    }
                }
            }
        }
    }
)
async def read_avaliacoes_game(
    qtd: int = Query(qtd=20, description="Número máximo de jogos a retornar"),
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
        Retorna os jogos mais populares ordenados por Hype Score.
        
        Parâmetros:
        - **qtd**: Número máximo de jogos a retornar (limite)
        - **page**: Número da página (via query params, padrão: 1)
        - **size**: Tamanho da página (via query params, padrão: 20)
        
        Retorna:
        - **items**: Lista de jogos com informações completas
        - **total**: Total de jogos disponíveis
        - **page**: Página atual
        - **size**: Tamanho da página
        
        Os jogos são ordenados do maior para o menor Hype Score.
    """
    params.size = qtd
    query = game_service.get_top_hyped_games()
    return await paginate_async(db, query, params)
