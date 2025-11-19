from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id", ondelete="CASCADE"))
    
    comentario = Column(Text)
    nota = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="avaliacoes")
    game = relationship("Game", back_populates="avaliacoes")
