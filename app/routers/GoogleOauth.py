from fastapi import APIRouter, Request, Depends
from app.core.auth_config import oauth  
from app.services.autentication.Google import GoogleAuthService
from app.database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Google Auth"])

@router.get(
    "/login",
    summary="Login com Google",
    description="Inicia o fluxo de autenticação OAuth2 com o Google. Redireciona o usuário para a página de login do Google.",
    responses={
        307: {
            "description": "Redirecionamento para o Google"
        }
    }
)
async def login(request: Request):
    """
        Inicia o fluxo de login com Google.
        
        Redireciona o usuário para a página de consentimento do Google.
        Após o login, o Google redirecionará de volta para /auth/google.
    """
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get(
    "/auth/google",
    summary="Callback de Autenticação Google",
    description="Recebe o código de autorização do Google, troca por tokens e autentica o usuário.",
    responses={
        200: {
            "description": "Login realizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJ...",
                        "refresh_token": "eyJ...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Falha na autenticação",
            "content": {
                "application/json": {
                    "example": {"error": "Descrição do erro"}
                }
            }
        }
    }
)
async def auth_google(request: Request, db: Session = Depends(get_db)):
    """
        Processa o callback do Google.
        
        Verifica o código retornado, obtém informações do usuário do Google,
        cria ou atualiza o usuário no banco de dados e gera tokens JWT.
    """
    try:
        return await GoogleAuthService.handle_auth_callback(request, db)
        
    except Exception as e:
        return {"error": str(e)}