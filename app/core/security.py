from datetime import datetime, timedelta 
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError 
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import ValidationError
from uuid import UUID
from app.models.user import User
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.database.session import get_db 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> "User":
    token = credentials.credentials

    credentials_exception = UnauthorizedException(
        message="Não foi possível validar as credenciais",
    )

    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except (JWTError, ValidationError):
        raise credentials_exception

    try:
        user_uuid = UUID(user_id)
        result = await db.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()
    except ValueError:
         raise credentials_exception

    if user is None:
        raise credentials_exception

    return user