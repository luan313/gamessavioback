from fastapi import APIRouter, Security, Depends
from app.services.RAWG_service import rawg_service
from app.database.session import get_db
from app.utils.deps import verify_admin_access
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.AnyDeal_service import AnyDealService
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/backoffice", 
    tags=["backoffice"],
    dependencies=[Security(verify_admin_access)] 
)

@router.post("/sync-games")
async def sync_games(db: AsyncSession = Depends(get_db)):
    resultado = await rawg_service.seed_games_by_amount(db=db)
    print(resultado)


@router.post("/sync-all-prices")
async def sync_all_prices(
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    result = await AnyDealService.sync_all_games_prices(db)
    return result