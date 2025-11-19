from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base

class GameCategoria(Base):
    __tablename__ = "game_categoria"

    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id", ondelete="CASCADE"), primary_key=True)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categoria.id", ondelete="CASCADE"), primary_key=True)

    game = relationship("Game", back_populates="categorias")
    categoria = relationship("Categoria", back_populates="games")
