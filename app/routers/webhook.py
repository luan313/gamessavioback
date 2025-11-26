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

@router.post("/webhook/notificar-games", status_code=200)
async def notification(payload: PriceUpdatePayload, db: AsyncSession = Depends(get_db)):
    try:
        count = await process_price_updates(payload.game_ids, db)
        return {"mensagem": "Todos os usuarios com games monitorados dentro do preço alvo foram notificados", "qtd_notificacao": count}
    except Exception as e:
        print(f"Error ao rodar o envio de email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error processing webhook")
