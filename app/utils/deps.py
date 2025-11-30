from fastapi import Header
from app.core.config import settings
from app.core.exceptions import ForbiddenException

async def verify_admin_access(x_admin_token: str = Header(...)):
    if x_admin_token != settings.BACKOFFICE_TOKEN:
        raise ForbiddenException(
            message="Acesso negado: Chave de Backoffice inválida."
        )