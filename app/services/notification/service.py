from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.jogos_monitorados import JogosMonitorados
from app.models.game import Game
from app.models.user import User
import logging
from app.services.notification.email_provider import EmailNotificationProvider
from app.services.notification.EmailTemplates import email_templates

async def process_price_updates(game_ids: List[UUID], db: AsyncSession, logger = None) -> int:
    """
        Processa atualizações de preços para jogos monitorados.
        
        Args:
            game_ids (List[UUID]): Lista de IDs dos jogos a serem monitorados
            db (AsyncSession): Sessão assíncrona do banco de dados
            logger: Logger para registro de eventos
        
        Returns:
            int: Número de notificações enviadas
    """
    if logger is None:
        logger = logging.getLogger(__name__)
        
    notification_provider = EmailNotificationProvider()
        
    stmt = (
        select(JogosMonitorados, Game, User)
        .join(Game, JogosMonitorados.game_id == Game.id)
        .join(User, JogosMonitorados.user_id == User.id)
        .where(JogosMonitorados.game_id.in_(game_ids))
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    notifications_sent = 0
    
    for monitoramento, game, user in rows:
        logger.info(f"Verificando jogo {game.nome} : {monitoramento.preco_alvo} - {game.last_price} | para o usuário {user.email}")
        
        if game.last_price is not None and game.last_price <= monitoramento.preco_alvo:
            logger.info(f"Enviando notificação para {user.email} - Game: {game.nome}")
            subject = f"🔥 Preço Baixou: {game.nome} por R$ {game.last_price:.2f}!"
            
            html_content = email_templates.prepare_content_games_notification(
                user_name=user.nome,
                game_name=game.nome,
                current_price=float(game.last_price),
                target_price=float(monitoramento.preco_alvo),
                deal_url=game.deal_url or "#",
                image_url=game.imagem_capa
            )
            
            success = await notification_provider.send(
                recipient=user.email,
                subject=subject,
                content=html_content
            )
            
            if success:
                notifications_sent += 1
            
    return notifications_sent

