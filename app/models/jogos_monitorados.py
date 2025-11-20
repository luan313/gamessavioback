from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from sqlalchemy.sql import func

from app.database.base import Base

class JogosMonitorados(Base):
    __tablename__ = "jogos_monitorados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id", ondelete="CASCADE"))
    preco_alvo = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "game_id"),)

    user = relationship("User", back_populates="monitorados")
    game = relationship("Game", back_populates="monitorados")
