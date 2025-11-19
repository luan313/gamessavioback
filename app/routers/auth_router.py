from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

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
@router.post("/register", response_model=TokenResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    access, refresh = AuthService.register_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    access, refresh = AuthService.login_user(data, db)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: TokenRefreshRequest):
    access, refresh = AuthService.refresh_token(data.refresh_token)
    return TokenResponse(access_token=access, refresh_token=refresh)