from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.game import TopHypedGamesResponse
from app.services import game_service
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_async
from fastapi_pagination import Page, Params

router = APIRouter(prefix="/game")

@router.get(
    "/hyped-games", 
    response_model=Page[TopHypedGamesResponse],
    summary="Listar jogos populares",
    description="Retorna uma lista de jogos ordenados pelo 'Hype Score', com paginação.",
)
async def read_avaliacoes_game(
    qtd: int,
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db)
):
    query = game_service.get_top_hyped_games(db, limit=qtd)
    return await paginate_async(db, query, params)
