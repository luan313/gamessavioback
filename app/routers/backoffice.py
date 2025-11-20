from fastapi import APIRouter, Security, Depends
from sqlalchemy.orm import Session
from app.services.RAWG_service import rawg_service
from app.database.session import get_db
from app.utils.deps import verify_admin_access

router = APIRouter(
    prefix="/backoffice", 
    tags=["backoffice"],
    dependencies=[Security(verify_admin_access)] 
)

@router.post("/sync-games")
async def sync_games(db: Session = Depends(get_db)):
    resultado = await rawg_service.seed_games_by_amount(db=db)
    print(resultado)

