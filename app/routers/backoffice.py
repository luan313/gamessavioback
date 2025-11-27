from fastapi import APIRouter, Security, Depends, status
from app.services.rawg import rawg_service
from app.database.session import get_db
from app.utils.deps import verify_admin_access
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.anydeal import AnyDealService
from app.services.backoffice import BackOfficeService
from app.schemas.jogos_monitorados import MonitoramentoBasicResponse
from fastapi import BackgroundTasks
import logging

logger = logging.getLogger(__name__)

admin_responses = {
    401: {"description": "Não autenticado"},
    403: {"description": "Proibido: Requer privilégios de Administrador"}
}

router = APIRouter(
    prefix="/backoffice", 
    tags=["backoffice"],
    dependencies=[Security(verify_admin_access)],
    responses=admin_responses
)

@router.post(
    "/sync-games",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar jogos da API RAWG",
    description="Importa/atualiza jogos do banco de dados a partir da API RAWG. Busca jogos populares e os adiciona ao sistema com informações completas (nome, descrição, metacritic, categorias, plataformas, etc.).",
    responses={
        200: {
            "description": "Sincronização executada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "jogos_importados": 50,
                        "jogos_atualizados": 10,
                        "mensagem": "Sincronização de jogos concluída"
                    }
                }
            }
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {
                    "example": {"detail": "Autenticação necessária"}
                }
            }
        },
        403: {
            "description": "Proibido - requer privilégios de administrador",
            "content": {
                "application/json": {
                    "example": {"detail": "Acesso negado: apenas administradores"}
                }
            }
        }
    }
)
async def sync_games(db: AsyncSession = Depends(get_db)):
    """
        Sincroniza jogos da API RAWG para o banco de dados.
        
        Funcionamento:
        - Busca jogos populares da API RAWG
        - Importa informações completas (nome, descrição, metacritic, hype, etc.)
        - Associa categorias e plataformas automaticamente
        - Atualiza jogos existentes se houver mudanças
        
        Retorna:
        - Relatório da sincronização com número de jogos importados/atualizados
        
        Uso:
        - Execute periodicamente para manter catálogo atualizado
        - Processo pode demorar alguns minutos dependendo da quantidade
        
        Requer autenticação: Sim (Bearer token) + Privilégios de Admin
    """
    resultado = await rawg_service.seed_games_by_amount(db=db)
    logger.info(resultado)
    return resultado


@router.post(
    "/sync-all-prices",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar preços de todos os jogos",
    description="Atualiza os preços de todos os jogos cadastrados consultando a API IsThereAnyDeal. Busca as melhores ofertas disponíveis e atualiza preços, lojas e URLs de compra.",
    responses={
        200: {
            "description": "Sincronização de preços executada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "precos_atualizados": 120,
                        "falhas": 5,
                        "mensagem": "Sincronização de preços concluída"
                    }
                }
            }
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {
                    "example": {"detail": "Autenticação necessária"}
                }
            }
        },
        403: {
            "description": "Proibido - requer privilégios de administrador",
            "content": {
                "application/json": {
                    "example": {"detail": "Acesso negado: apenas administradores"}
                }
            }
        }
    }
)
async def sync_all_prices(
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    """
        Sincroniza preços de todos os jogos via API IsThereAnyDeal.
        
        Funcionamento:
        - Busca todos os jogos cadastrados no banco
        - Consulta preços atualizados na API IsThereAnyDeal
        - Atualiza informações de preço, loja e URL de compra
        - Cria histórico de preços para tracking
        - Executa em background para não bloquear
        
        Retorna:
        - Relatório com número de preços atualizados e eventuais falhas
        
        Uso:
        - Execute diariamente ou semanalmente para manter preços atualizados
        - Essencial para funcionalidade de alertas de preço
        - Processo pode demorar bastante tempo (roda em background)
        
        Requer autenticação: Sim (Bearer token) + Privilégios de Admin
    """
    result = await AnyDealService.sync_all_games_prices(db)
    return result



@router.get(
    "/games/all",
    response_model=list[MonitoramentoBasicResponse],
    summary="Listar todos os jogos monitorados",
    description="Retorna uma lista de todos os jogos monitorados no sistema.",
    responses={
        200: {
            "description": "Lista de jogos monitorados"
        }
    }
)
async def get_all_games(db: AsyncSession = Depends(get_db)):
    return await BackOfficeService.get_all_games(db)