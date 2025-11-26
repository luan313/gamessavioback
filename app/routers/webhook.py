from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.webhook import PriceUpdatePayload
from app.services.notification_service import process_price_updates
from app.utils.deps import verify_admin_access
import logging

admin_responses = {
    401: {"description": "Não autenticado"},
    403: {"description": "Proibido: Requer privilégios de Administrador"}
}

router = APIRouter(    
    dependencies=[Security(verify_admin_access)],
    responses=admin_responses
)
logger = logging.getLogger(__name__)

@router.post("/webhook/price-update", status_code=200)
async def handle_price_update(payload: PriceUpdatePayload, db: AsyncSession = Depends(get_db)):
    """
        Webhook to receive game price updates.
        Triggers notifications for users monitoring these games if the price target is met.
    """
    try:
        count = await process_price_updates(payload.game_ids, db)
        return {"message": "Price updates processed", "notifications_sent": count}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error processing webhook")
