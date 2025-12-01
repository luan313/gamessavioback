from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/me", 
    response_model=UserResponse,
    summary="Obter meu perfil",
    description="Retorna as informações do perfil do usuário autenticado.",
    responses={
        200: {
            "description": "Perfil retornado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "nome": "João Silva",
                        "email": "joao@example.com",
                        "created_at": "2024-11-24T18:00:00"
                    }
                }
            }
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {
                    "example": {"error": True, "message": "Não foi possível validar as credenciais", "details": None}
                }
            }
        }
    }
)
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """
        Retorna os dados do perfil do usuário autenticado.
        
        Retorna:
        - **id**: UUID do usuário
        - **nome**: Nome completo
        - **email**: Endereço de email cadastrado
        - **created_at**: Data e hora do cadastro
        
        Uso:
        - Usado para exibir informações do perfil no frontend
        - Validar se o token atual ainda é válido
        
        Requer autenticação: Sim (Bearer token)
    """
    return current_user
