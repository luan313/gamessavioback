from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import (
    TokenResponse, TokenRefreshRequest
)
from app.schemas.user import (
    UserCreate,
    UserLogin
)
from app.services.auth_service import AuthService
from app.database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register", 
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
    description="Registra um novo usuário no sistema e retorna os tokens de acesso (Access e Refresh).",
    responses={
        409: {"description": "Email já cadastrado"},
        400: {"description": "Dados inválidos"}
    }
)
async def register_user(data: UserCreate, db: Session = Depends(get_db)):
    access, refresh = await AuthService.register_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="Autenticação de Usuário",
    description="Valida as credenciais (email/senha) e retorna tokens JWT.",
    responses={
        401: {"description": "Credenciais inválidas (Email ou senha incorretos)"},
        404: {"description": "Usuário não encontrado"}
    }
)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    access, refresh = await AuthService.login_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post(
    "/refresh", 
    response_model=TokenResponse,
    summary="Renovar Token de Acesso",
    description="Gera um novo Access Token usando um Refresh Token válido.",
    responses={
        401: {"description": "Refresh Token inválido ou expirado"}
    }
)
async def refresh_token(data: TokenRefreshRequest):
    access, refresh = await AuthService.refresh_token(data.refresh_token)
    return TokenResponse(access_token=access, refresh_token=refresh)