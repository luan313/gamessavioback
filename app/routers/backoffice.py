from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.RAWG_service import rawg_service
from app.database.session import get_db
    

router = APIRouter(prefix="/backoffice", tags=["backoffice"])
@router.get("/sync-games")
def sync_games(db: Session = Depends(get_db)):
    resultado = rawg_service.seed_games_by_amount(db=db)
    print(resultado)

