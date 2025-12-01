from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.webhook import PriceUpdatePayload
from app.services.notification import process_price_updates
from app.utils.deps import verify_admin_access
import logging

from app.core.docs import admin_responses

logger = logging.getLogger(__name__)


router = APIRouter(    
    dependencies=[Security(verify_admin_access)],
    responses=admin_responses
)


@router.post(
    "/webhook/notificar-games", 
    status_code=200,
    summary="Webhook - Notificação de preços",
    description="Endpoint chamado externamente (ex: GitHub Actions) para processar atualizações de preços e notificar usuários. Requer token de administrador.",
    responses={
        200: {
            "description": "Processamento concluído com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Todos os usuarios com games monitorados dentro do preço alvo foram notificados",
                        "qtd_notificacao": 5
                    }
                }
            }
        },
        500: {
            "description": "Erro interno no processamento",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal Server Error processing webhook"}
                }
            }
        }
    }
)
async def notification(payload: PriceUpdatePayload, db: AsyncSession = Depends(get_db)) -> dict:
    """
        Processa notificações de preços via webhook.
        
        Este endpoint é acionado por um serviço externo (como um cron job ou GitHub Action)
        para verificar se algum jogo monitorado atingiu o preço alvo e enviar emails aos usuários.
        
        Parâmetros:
        - **payload**: Lista de IDs de jogos que tiveram atualização de preço
        
        Retorna:
        - Resumo do processamento com quantidade de notificações enviadas
        
        Requer autenticação: Sim (Privilégios de Admin)
    """
    count = await process_price_updates(payload.game_ids, db)
    return {"mensagem": "Todos os usuarios com games monitorados dentro do preço alvo foram notificados", "qtd_notificacao": count}
