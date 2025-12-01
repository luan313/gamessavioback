from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from app.models.jogos_monitorados import JogosMonitorados
from app.schemas.jogos_monitorados import MonitoramentoCreate, MonitoramentoUpdate
from sqlalchemy.orm import selectinload
from app.core.exceptions import ForbiddenException, NotFoundException

class MonitoramentoService:
    @staticmethod
    async def create_monitoramento(db: AsyncSession, monitoramento: MonitoramentoCreate, user_id: UUID) -> JogosMonitorados:
        """
            Cria um novo monitoramento para um jogo.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                monitoramento (MonitoramentoCreate): Dados do monitoramento a ser criado.
                user_id (UUID): ID do usuário que está criando o monitoramento.
            
            Returns:
                JogosMonitorados: Monitoramento criado.
        """
        db_monitoramento = JogosMonitorados(
            preco_alvo = monitoramento.preco_alvo,
            game_id=monitoramento.game_id, 
            user_id=user_id
        )

        db.add(db_monitoramento)
        await db.commit()
        
        query = (
            select(JogosMonitorados)
            .options(selectinload(JogosMonitorados.game))  
            .where(JogosMonitorados.id == db_monitoramento.id)
        )
        
        result = await db.execute(query)
        monitoramento_criado = result.scalars().first()
        
        return monitoramento_criado


    @staticmethod
    async def get_monitored_games_for_user(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> list[JogosMonitorados]:
        """
            Retorna todos os jogos monitorados por um usuário.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                user_id (UUID): ID do usuário.
                skip (int): Número de registros a serem pulados.
                limit (int): Número máximo de registros a serem retornados.
            
            Returns:
                list[JogosMonitorados]: Lista de jogos monitorados.
        """
        result = await db.execute(
            select(JogosMonitorados)
            .options(selectinload(JogosMonitorados.game))
            .where(JogosMonitorados.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


    @staticmethod
    async def get_monitoramento_by_id(db: AsyncSession, monitoramento_id: UUID) -> JogosMonitorados | None:
        """
            Retorna um monitoramento por ID.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                monitoramento_id (UUID): ID do monitoramento.
            
            Returns:
                JogosMonitorados | None: Monitoramento encontrado ou None se não encontrado.
        """
        result = await db.execute(
            select(JogosMonitorados)
            .options(selectinload(JogosMonitorados.game))
            .where(JogosMonitorados.id == monitoramento_id))
        return result.scalar_one_or_none()
    

    @staticmethod
    async def update_monitoring(db: AsyncSession, monitoramento_id: UUID, monitoramento_update: MonitoramentoUpdate, user_id: UUID) -> JogosMonitorados:
        """
            Atualiza um monitoramento existente.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                monitoramento_id (UUID): ID do monitoramento a ser atualizado.
                monitoramento_update (MonitoramentoUpdate): Dados do monitoramento a serem atualizados.
                user_id (UUID): ID do usuário que está atualizando o monitoramento.
            
            Returns:
                JogosMonitorados: Monitoramento atualizado.
        """
        db_monitoramento = await MonitoramentoService.get_monitoramento_by_id(db, monitoramento_id)

        if not db_monitoramento:
            raise NotFoundException(message="Monitoramento não encontrado")

        if db_monitoramento.user_id != user_id:
            raise ForbiddenException(message="Não autorizado a editar este monitoramento")

        if monitoramento_update.preco_alvo is not None:
            db_monitoramento.preco_alvo = monitoramento_update.preco_alvo

        await db.commit()
        await db.refresh(db_monitoramento)
        return db_monitoramento
    
    
    @staticmethod
    async def delete_monitoramento(db: AsyncSession, monitoramento_id: UUID, user_id: UUID) -> bool:
        """
            Remove um monitoramento existente.
            
            Args:
                db (AsyncSession): Sessão assíncrona do banco de dados.
                monitoramento_id (UUID): ID do monitoramento a ser removido.
                user_id (UUID): ID do usuário que está removendo o monitoramento.
            
            Returns:
                bool: True se o monitoramento foi removido com sucesso.
        """
        db_monitoramento = await MonitoramentoService.get_monitoramento_by_id(db, monitoramento_id)
        
        if not db_monitoramento:
            raise NotFoundException(message="Monitoramento não encontrado")
        
        if db_monitoramento.user_id != user_id:
            raise ForbiddenException(message="Não autorizado a remover este monitoramento")

        await db.delete(db_monitoramento)
        await db.commit()
        return True