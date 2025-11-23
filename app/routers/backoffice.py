from fastapi import APIRouter, Security, Depends, status
from app.services.RAWG_service import rawg_service
from app.database.session import get_db
from app.utils.deps import verify_admin_access
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.AnyDeal_service import AnyDealService
from fastapi import BackgroundTasks

admin_responses = {
    401: {"description": "Não autenticado"},
    403: {"description": "Proibido: Requer privilégios de Administrador"}
}

router = APIRouter(
    prefix="/backoffice", 
    tags=["backoffice"],
    dependencies=[Security(verify_admin_access)],
    responses=admin_responses
)

@router.post(
    "/sync-games",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar Jogos (RAWG)",
    description="Dispara a importação/seed de jogos a partir da API externa RAWG baseada em uma quantidade pré-definida.",
)
async def sync_games(db: AsyncSession = Depends(get_db)):
    resultado = await rawg_service.seed_games_by_amount(db=db)
    print(resultado)


@router.post(
    "/sync-all-prices",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar Preços (AnyDeal)",
    description="Atualiza os preços de todos os jogos cadastrados consultando a API de ofertas.",
)
async def sync_all_prices(
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    result = await AnyDealService.sync_all_games_prices(db)
    return result