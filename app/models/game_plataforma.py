from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base

class GamePlataforma(Base):
    __tablename__ = "game_plataforma"

    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id"), primary_key=True)
    plataforma_id = Column(UUID(as_uuid=True), ForeignKey("plataforma.id"), primary_key=True)

    game = relationship("Game", back_populates="plataformas")
    plataforma = relationship("Plataforma", back_populates="games")