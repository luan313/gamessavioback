from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    """
        Interface base para provedores de notificação.
    """
    
    @abstractmethod
    async def send(self, recipient: str, subject: str, content: str, **kwargs) -> bool:
        """
            Envia uma notificação.
            
            Args:
                recipient (str): Destinatário da notificação (email, telefone, etc)
                subject (str): Assunto da notificação
                content (str): Conteúdo da notificação
                **kwargs: Argumentos adicionais específicos do provedor
                
            Returns:
                bool: True se enviado com sucesso, False caso contrário
        """
        pass
