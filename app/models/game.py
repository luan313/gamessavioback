from sqlalchemy import Column, String, Text, Numeric, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Column, String, Text, Numeric, DECIMAL, Integer, Date, DateTime, ForeignKey
from app.database.base import Base
from sqlalchemy.sql import func

class Game(Base):
    __tablename__ = "game"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    slug = Column(String(255))                
    descricao = Column(Text)
    
    
    imagem_capa = Column(String(500))        
    nota_media = Column(Numeric(3, 2))        
    metacritic = Column(Integer)              
    data_lancamento = Column(Date)
    
    last_price = Column(DECIMAL(10,2), default=0.00)
    isthereanydeal_id = Column(String(200))
    rawg_id = Column(Integer, unique=True)
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    categorias = relationship("GameCategoria", back_populates="game", cascade="all, delete-orphan")
    plataformas = relationship("GamePlataforma", back_populates="game", cascade="all, delete-orphan") # Novo
    avaliacoes = relationship("Avaliacao", back_populates="game", cascade="all, delete-orphan")
    monitorados = relationship("JogosMonitorados", back_populates="game", cascade="all, delete-orphan")
    historico_precos = relationship("HistoricoPreco", back_populates="game", cascade="all, delete-orphan")