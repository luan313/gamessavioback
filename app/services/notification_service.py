import smtplib
from email.message import EmailMessage
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.jogos_monitorados import JogosMonitorados
from app.models.game import Game
from app.models.user import User
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_email(to_email: str, subject: str, content: str):
    if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not set. Skipping email sending.")
        logger.info(f"Would send email to {to_email}: {subject}")
        return

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


async def process_price_updates(game_ids: List[UUID], db: AsyncSession):
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
        if game.last_price is not None and game.last_price <= monitoramento.preco_alvo:
            subject = f"Price Alert: {game.nome} is now {game.last_price}!"
            content = (
                f"Olá {user.nome},\n\n"
                f"Boas notícias! O jogo {game.nome} baixou para {game.last_price}.\n"
                f"Seu preço alvo era {monitoramento.preco_alvo}.\n\n"
                f"Confira aqui: {game.deal_url or 'Link não disponível'}\n\n"
                "Boas jogatinas!"
            )
            await send_email(user.email, subject, content)
            notifications_sent += 1
            
    return notifications_sent
