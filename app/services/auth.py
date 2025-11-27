from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select                   
from jose import jwt, JWTError
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
)
from app.core.config import settings
from app.models.user import User

class AuthService:
    @staticmethod
    async def register_user(data, db: AsyncSession) -> tuple[str, str]:
        """
            Registra um novo usuário no sistema.

            Verifica se o email já está em uso, cria o novo usuário com senha hash,
            salva no banco de dados e retorna os tokens de acesso e refresh.

            Args:
                data: Dados do usuário para registro (nome, email, password).
                db (AsyncSession): Sessão assíncrona do banco de dados.

            Returns:
                tuple[str, str]: Uma tupla contendo (access_token, refresh_token).

            Raises:
                HTTPException: Se o email já estiver em uso.
        """
        query = select(User).where(User.email == data.email)
        result = await db.execute(query)
        existing = result.scalar_one_or_none()

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
        
        await db.commit()
        await db.refresh(new_user)

        access = create_access_token({"sub": str(new_user.id)})
        refresh = create_refresh_token({"sub": str(new_user.id)})

        return access, refresh


    @staticmethod
    async def login_user(data, db: AsyncSession) -> tuple[str, str]:
        """
            Autentica um usuário no sistema.

            Busca o usuário pelo email, verifica a senha e, se válidos,
            retorna os tokens de acesso e refresh.

            Args:
                data: Dados de login (email, password).
                db (AsyncSession): Sessão assíncrona do banco de dados.

            Returns:
                tuple[str, str]: Uma tupla contendo (access_token, refresh_token).

            Raises:
                HTTPException: Se o email ou senha estiverem incorretos.
        """
        query = select(User).where(User.email == data.email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos."
            )

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return access, refresh


    @staticmethod
    def refresh_token(refresh_token: str) -> tuple[str, str]:
        """
            Renova os tokens de acesso a partir de um refresh token válido.

            Decodifica o refresh token para obter o ID do usuário e gera
            novos tokens de acesso e refresh.

            Args:
                refresh_token (str): O token de atualização (refresh token).

            Returns:
                tuple[str, str]: Uma tupla contendo (novo_access_token, novo_refresh_token).

            Raises:
                HTTPException: Se o refresh token for inválido ou expirado.
        """
        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
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