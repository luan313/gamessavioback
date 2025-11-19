from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
)
from app.models.user import User


class AuthService:

    @staticmethod
    def register_user(data, db: Session):
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso."
            )

        new_user = User(
            nome=data.nome,
            email=data.email,
            password_hash=hash_password(data.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access = create_access_token({"sub": str(new_user.id)})
        refresh = create_refresh_token({"sub": str(new_user.id)})

        return access, refresh

    @staticmethod
    def login_user(data, db: Session):
        user = db.query(User).filter(User.email == data.email).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos."
            )

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return access, refresh

    @staticmethod
    def refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token,
                REFRESH_SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido."
            )

        new_access = create_access_token({"sub": user_id})
        new_refresh = create_refresh_token({"sub": user_id})

        return new_access, new_refresh
