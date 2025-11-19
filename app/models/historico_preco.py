from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class HistoricoPreco(Base):
    __tablename__ = "historico_preco"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id", ondelete="CASCADE"))
    preco = Column(DECIMAL(10,2), nullable=False)
    loja = Column(String(120))
    data_coleta = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="historico_precos")
