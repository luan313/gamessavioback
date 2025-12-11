
from app.services.User import UserService
from app.schemas.user import UserBasic, UserGoogleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from fastapi import Request
from app.core.auth_config import oauth
from app.core.security import create_access_token
from typing import Dict, Any

class GoogleAuthService:

    @staticmethod
    async def register_user(user: UserGoogleCreate, db: AsyncSession) -> UserBasic:
        """
            Registra um novo usuário no sistema com dados do Google.

            Args:
                user (UserGoogleCreate): Dados do usuário recebidos do Google.
                db (AsyncSession): Sessão do banco de dados.

            Returns:
                UserBasic: Objeto do usuário criado.
        """
        new_user = User(
            nome=user.nome,
            email=user.email,
            google_id=user.google_id,
            avatar_url=user.avatar_url,
        )
        
        db.add(new_user) 
        
        await db.commit()
        await db.refresh(new_user)
        return UserBasic.from_orm(new_user)


    @staticmethod
    async def update_user(db_user: User, user_data: UserGoogleCreate, db: AsyncSession) -> UserBasic:
        """
            Atualiza os dados de um usuário existente com informações do Google.

            Args:
                db_user (User): Usuário existente no banco de dados.
                user_data (UserGoogleCreate): Novos dados recebidos do Google.
                db (AsyncSession): Sessão do banco de dados.

            Returns:
                UserBasic: Objeto do usuário atualizado.
        """
        db_user.google_id = user_data.google_id
        db_user.avatar_url = user_data.avatar_url
        db_user.nome = user_data.nome

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)        
        return UserBasic.from_orm(db_user)

    @staticmethod
    async def handle_auth_callback(request: Request, db: AsyncSession) -> Dict[str, Any]:
        """
            Processa o callback de autenticação do Google.

            Troca o código de autorização por tokens, obtém informações do usuário,
            registra ou atualiza o usuário no banco e gera um token de acesso JWT.

            Args:
                request (Request): Requisição HTTP contendo o código de autorização.
                db (AsyncSession): Sessão do banco de dados.

            Returns:
                Dict[str, Any]: Dicionário contendo o usuário, token de acesso e tipo do token.
            
            Raises:
                ValueError: Se não for possível obter os dados do usuário do Google.
        """
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')

        if not user_info:
            raise ValueError("Não foi possível obter dados do Google")
        
        user = UserGoogleCreate(
            nome=user_info.get('name'),
            email=user_info.get('email'),
            google_id=user_info.get('sub'),
            avatar_url=user_info.get('picture'),
        )    
    
        db_user = await UserService.GetUserByEmail(user_info.get('email'), db)
                
        if not db_user:
            final_user = await GoogleAuthService.register_user(user, db)
            
        else:
            final_user = await GoogleAuthService.update_user(db_user, user, db)


        access_token = create_access_token({"sub": str(final_user.id)})
        return {
            "user": final_user, 
            "access_token": token.get('access_token'),
            "token_type": "bearer"
        }