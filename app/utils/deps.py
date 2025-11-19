from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_admin_access(x_admin_token: str = Header(...)):
    if x_admin_token != settings.BACKOFFICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Chave de Backoffice inválida."
        )