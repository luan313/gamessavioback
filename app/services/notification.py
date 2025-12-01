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
        <html lang="pt-BR">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Alerta de Preço - GamesSavio</title>
            <style>
                /* Reset styles */
                body {{ margin: 0; padding: 0; min-width: 100%; width: 100% !important; height: 100% !important; }}
                body, table, td, div, p, a {{ -webkit-font-smoothing: antialiased; text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; line-height: 100%; }}
                table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse !important; border-spacing: 0; }}
                img {{ border: 0; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }}
                
                /* Responsive styles */
                @media screen and (max-width: 600px) {{
                    .email-container {{ width: 100% !important; max-width: 100% !important; }}
                    .fluid-img {{ height: auto !important; max-width: 100% !important; width: 100% !important; }}
                    .padding-mobile {{ padding: 15px !important; }}
                    .text-mobile {{ font-size: 14px !important; }}
                    .header-mobile {{ font-size: 20px !important; }}
                    .price-mobile {{ font-size: 28px !important; }}
                    .cta-button {{ display: block !important; width: 100% !important; box-sizing: border-box !important; text-align: center !important; }}
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 0; background-color: {bg_color}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: {text_color};">
            <center style="width: 100%; background-color: {bg_color};">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: {bg_color}; width: 100%; margin: 0 auto;">
                    <tr>
                        <td align="center" style="padding: 20px 10px;">
                            <!-- Main Container -->
                            <table role="presentation" class="email-container" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: {card_bg}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); width: 100%; max-width: 600px; margin: 0 auto;">
                                
                                <!-- Image Section -->
                                <tr>
                                    <td style="padding: 0; background-color: #000; text-align: center;">
                                        {f'<img src="{image_url}" alt="{game_name}" class="fluid-img" style="width: 100%; height: auto; display: block; max-height: 200px; object-fit: cover; border: 0;">' if image_url else ''}
                                    </td>
                                </tr>

                                <!-- Content Section -->
                                <tr>
                                    <td class="padding-mobile" style="padding: 25px 20px;">
                                        <h1 class="header-mobile" style="margin: 0 0 15px 0; font-size: 22px; color: {text_color}; text-align: center;">Preço Atingido! 🎯</h1>
                                        
                                        <p class="text-mobile" style="margin: 0 0 15px 0; font-size: 15px; line-height: 1.5; color: #cbd5e1;">
                                            Olá <strong>{user_name}</strong>, o jogo <strong>{game_name}</strong> atingiu seu preço alvo.
                                        </p>

                                        <!-- Price Box -->
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 20px;">
                                            <tr>
                                                <td style="padding: 15px; text-align: center;">
                                                    <p style="margin: 0 0 5px 0; font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Preço Atual</p>
                                                    <p class="price-mobile" style="margin: 0; font-size: 32px; font-weight: bold; color: {accent_color};">R$ {current_price:.2f}</p>
                                                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #94a3b8;">Seu alvo: R$ {target_price:.2f}</p>
                                                </td>
                                            </tr>
                                        </table>

                                        <!-- CTA Button -->
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td align="center">
                                                    <a href="{deal_url}" class="cta-button" style="display: inline-block; padding: 14px 28px; background-color: {primary_color}; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; transition: background-color 0.3s; width: auto; min-width: 180px; text-align: center;">
                                                        Ver Oferta
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin: 20px 0 0 0; font-size: 12px; color: #64748b; text-align: center; line-height: 1.4;">
                                            *Verifique a loja para confirmar.
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="padding: 15px; background-color: #0f172a; text-align: center; border-top: 1px solid #334155;">
                                        <p style="margin: 0; font-size: 11px; color: #64748b;">
                                            &copy; 2024 GamesSavio.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </center>
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
