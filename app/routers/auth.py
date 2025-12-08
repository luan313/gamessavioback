from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from app.schemas.auth import (
    TokenResponse, TokenRefreshRequest
)
from app.schemas.user import (
    UserCreate,
    UserLogin
)
from app.services.autentication.Default import AuthService
from app.database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", 
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário no sistema. Após o registro bem-sucedido, retorna automaticamente os tokens de autenticação (Access Token e Refresh Token).",
    responses={
        201: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Dados inválidos ou email já cadastrado",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Email já está em uso.", "details": None}
                }
            }
        }
    }
)
async def register_user(data: UserCreate, db: Session = Depends(get_db), _ = Depends(RateLimiter(times=5, seconds=60))) -> TokenResponse:
    """
        Registra um novo usuário no sistema.
        
        Parâmetros:
        - **email**: Email válido (será usado para login)
        - **password**: Senha com no mínimo 8 caracteres
        - **username**: Nome de usuário (opcional)
        
        Retorna:
        - **access_token**: Token JWT para autenticação em endpoints protegidos (expira em 30 minutos)
        - **refresh_token**: Token para renovar o access_token (expira em 7 dias)
        - **token_type**: Tipo do token (sempre "bearer")
        
        Regras:
        - Email deve ser único no sistema
        - Senha é criptografada antes de ser armazenada
        - Tokens são retornados automaticamente após registro
        
        Não requer autenticação: Endpoint público
    """
    access, refresh = await AuthService.register_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="Login - Autenticação de usuário",
    description="Autentica um usuário com email e senha. Retorna tokens JWT (Access Token e Refresh Token) para uso em endpoints protegidos.",
    responses={
        200: {
            "description": "Login realizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Credenciais inválidas - email ou senha incorretos",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Email ou senha incorretos.", "details": None}
                }
            }
        }
    }
)
async def login(data: UserLogin, db: Session = Depends(get_db), _ = Depends(RateLimiter(times=5, seconds=60))) -> TokenResponse:
    """
        Autentica um usuário no sistema.
        
        Parâmetros:
        - **email**: Email cadastrado do usuário
        - **password**: Senha da conta
        
        Retorna:
        - **access_token**: Token JWT para usar em requisições autenticadas (expira em 30 minutos)
        - **refresh_token**: Token para renovar o access_token quando expirar (expira em 7 dias)
        - **token_type**: "bearer" - use como: Authorization: Bearer {access_token}
        
        Como usar o token:
        1. Faça login para receber os tokens
        2. Inclua o access_token no header: `Authorization: Bearer {access_token}`
        3. Quando o access_token expirar, use o refresh_token no endpoint /refresh
        
        Não requer autenticação: Endpoint público
    """
    access, refresh = await AuthService.login_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post(
    "/refresh", 
    response_model=TokenResponse,
    summary="Renovar tokens de autenticação",
    description="Gera um novo par de tokens (Access Token e Refresh Token) usando um Refresh Token válido. Use este endpoint quando o Access Token expirar.",
    responses={
        200: {
            "description": "Tokens renovados com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Refresh Token inválido, expirado ou revogado",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Refresh token inválido.", "details": None}
                }
            }
        }
    }
)
async def refresh_token(data: TokenRefreshRequest, _ = Depends(RateLimiter(times=10, seconds=60))) -> TokenResponse:
    """
        Renova os tokens de autenticação usando um Refresh Token.
        
        Parâmetros:
        - **refresh_token**: Refresh Token válido obtido no login ou registro
        
        Retorna:
        - **access_token**: Novo Access Token (expira em 30 minutos)
        - **refresh_token**: Novo Refresh Token (expira em 7 dias)
        - **token_type**: "bearer"
        
        Quando usar:
        - Quando receber erro 401 (Unauthorized) em endpoints protegidos
        - Antes do Access Token expirar (recomendado renovar após 25 minutos)
        - Para manter o usuário logado sem solicitar nova senha
        
        Fluxo recomendado:
        1. Detectar expiração do Access Token
        2. Enviar Refresh Token para este endpoint
        3. Atualizar tokens armazenados com os novos valores
        4. Repetir requisição original com novo Access Token
        
        Não requer autenticação: Apenas o Refresh Token válido
    """
    access, refresh = await AuthService.refresh_token(data.refresh_token)
    return TokenResponse(access_token=access, refresh_token=refresh)