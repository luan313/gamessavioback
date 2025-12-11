import smtplib
from email.message import EmailMessage
from app.core.config import settings
import logging
from app.services.notification.interfaces import NotificationProvider

class EmailNotificationProvider(NotificationProvider):
    """
        Implementação do provedor de notificação via Email.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def send(self, recipient: str, subject: str, content: str, **kwargs) -> bool:
        """
            Envia uma notificação via email.
            
            Args:
                recipient (str): Destinatário da notificação
                subject (str): Assunto da notificação
                content (str): Conteúdo da notificação
                **kwargs: Argumentos adicionais específicos do provedor
                
            Returns:
                bool: True se enviado com sucesso, False caso contrário
        """
        if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
            self.logger.warning("Email credentials not set. Skipping email sending.")
            self.logger.info(f"Would send email to {recipient}: {subject}")
            return False

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_USER
        msg["To"] = recipient
        
        msg.set_content("Seu cliente de email não suporta HTML. Por favor, visualize em um cliente compatível.")
        msg.add_alternative(content, subtype="html")

        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
                
                self.logger.info(f"Email sent to {recipient}")
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient}: {e}")
            return False
     