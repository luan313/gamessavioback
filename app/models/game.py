from sqlalchemy import Column, String, Text, Numeric, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database.base import Base

class Game(Base):
    __tablename__ = "game"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    nota_media = Column(Numeric(3, 2))
    last_price = Column(DECIMAL(10,2))
    isthereanydeal_id = Column(String(200))

    categorias = relationship("GameCategoria", back_populates="game")
    avaliacoes = relationship("Avaliacao", back_populates="game", cascade="all, delete")
    monitorados = relationship("JogosMonitorados", back_populates="game", cascade="all, delete")
    historico_precos = relationship("HistoricoPreco", back_populates="game", cascade="all, delete")
