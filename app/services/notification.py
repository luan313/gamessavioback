import smtplib
from email.message import EmailMessage
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.jogos_monitorados import JogosMonitorados
from app.models.game import Game
from app.models.user import User
from email.utils import make_msgid
from pathlib import Path
from app.core.config import settings
import logging

BASE_DIR = Path(__file__).resolve().parents[2]

def get_html_template(user_name: str, game_name: str, current_price: float, target_price: float, deal_url: str, image_url: str | None) -> str:
    """
        Gera um template HTML para notificação de preço baixado.
        
        Args:
            user_name (str): Nome do usuário
            game_name (str): Nome do jogo
            current_price (float): Preço atual do jogo
            target_price (float): Preço alvo do jogo
            deal_url (str): URL da oferta
            image_url (str | None): URL da imagem do jogo
        
        Returns:
            str: Template HTML
    """
    primary_color = "#7c3aed" 
    bg_color = "#0f172a"
    card_bg = "#1e293b" 
    text_color = "#f8fafc" 
    accent_color = "#10b981" 

    return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Alerta de Preço - GamesSavio</title>
        </head>
        <body style="margin: 0; padding: 0; background-color: {bg_color}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: {text_color};">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td align="center" style="padding: 40px 0;">
                        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: {card_bg}; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);">
                            
                            <tr>
                                <td style="padding: 0; background-color: #000; text-align: center;">
                                    {f'<img src="{image_url}" alt="{game_name}" style="width: 100%; height: auto; display: block; max-height: 300px; object-fit: cover;">' if image_url else ''}
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 40px 30px;">
                                    <h1 style="margin: 0 0 20px 0; font-size: 24px; color: {text_color};">Preço Atingido! 🎯</h1>
                                    
                                    <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.5; color: #cbd5e1;">
                                        Olá <strong>{user_name}</strong>,
                                    </p>
                                    
                                    <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.5; color: #cbd5e1;">
                                        Boas notícias! O jogo <strong>{game_name}</strong> atingiu o preço que você estava esperando.
                                    </p>

                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 30px;">
                                        <tr>
                                            <td style="padding: 20px; text-align: center;">
                                                <p style="margin: 0 0 5px 0; font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Preço Atual</p>
                                                <p style="margin: 0; font-size: 36px; font-weight: bold; color: {accent_color};">R$ {current_price:.2f}</p>
                                                <p style="margin: 10px 0 0 0; font-size: 14px; color: #94a3b8;">Seu alvo: R$ {target_price:.2f}</p>
                                            </td>
                                        </tr>
                                    </table>

                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                        <tr>
                                            <td align="center">
                                                <a href="{deal_url}" style="display: inline-block; padding: 16px 32px; background-color: {primary_color}; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; transition: background-color 0.3s;">
                                                    Ver Oferta Agora
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="margin: 30px 0 0 0; font-size: 14px; color: #64748b; text-align: center;">
                                        *Os preços podem variar rapidamente. Verifique a loja para confirmar.
                                    </p>
                                </td>
                            </tr>
                            
                            <tr>
                                <td style="padding: 20px; background-color: #0f172a; text-align: center; border-top: 1px solid #334155;">
                                    <p style="margin: 0; font-size: 12px; color: #64748b;">
                                        &copy; 2024 GamesSavio. Todos os direitos reservados.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
    """

async def send_email(to_email: str, subject: str, html_content: str, logger) -> None:
    """
        Envia um email para o usuário.
        
        Args:
            to_email (str): Email do destinatário
            subject (str): Assunto do email
            html_content (str): Conteúdo HTML do email
            logger: Logger para registro de eventos
        
        Returns:
            None
    """
    if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not set. Skipping email sending.")
        logger.info(f"Would send email to {to_email}: {subject}")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_USER
    msg["To"] = to_email
    
    msg.set_content("Seu cliente de email não suporta HTML. Por favor, visualize em um cliente compatível.")
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


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
            
            html_content = get_html_template(
                user_name=user.nome,
                game_name=game.nome,
                current_price=float(game.last_price),
                target_price=float(monitoramento.preco_alvo),
                deal_url=game.deal_url or "#",
                image_url=game.imagem_capa
            )
            
            await send_email(user.email, subject, html_content, logger)
            notifications_sent += 1
            
    return notifications_sent
