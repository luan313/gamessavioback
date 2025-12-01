from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.categoria import Categoria
from app.models.game_categoria import GameCategoria
from app.models.game import Game
from uuid import UUID
from app.core.exceptions import NotFoundException


class CategoriaService:
    @staticmethod
    async def get_categorias_com_quantidade_jogos(db: AsyncSession) -> list[dict]:
        """
        Retorna todas as categorias com a quantidade de jogos em cada uma.
        """
        query = (
            select(
                Categoria.id,
                Categoria.nome,
                Categoria.imagem,
                func.count(GameCategoria.game_id).label("quantidade_jogos")
            )
            .outerjoin(GameCategoria, Categoria.id == GameCategoria.categoria_id)
            .group_by(Categoria.id, Categoria.nome)
            .order_by(Categoria.nome)
        )
        
        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "id": r.id,
                "nome": r.nome,
                "imagem": r.imagem,
                "quantidade_jogos": r.quantidade_jogos,
            }
            for r in rows
        ]

    @staticmethod
    async def get_jogos_por_categoria(db: AsyncSession, categoria_id: UUID) -> list[Game]:
        """
            Retorna todos os jogos de uma categoria específica.
            
            Args:
                db: Sessão do banco de dados
                categoria_id: UUID da categoria
                
            Returns:
                Lista de jogos da categoria
                
            Raises:
                NotFoundException: Se a categoria não existir
        """
        # Verifica se categoria existe
        result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))

        if not result.scalar_one_or_none():
            raise NotFoundException(message="Categoria não encontrada")

        return (
            select(Game)
            .join(GameCategoria, Game.id == GameCategoria.game_id)
            .where(GameCategoria.categoria_id == categoria_id)
            .order_by(Game.nome)
        )
        
        
