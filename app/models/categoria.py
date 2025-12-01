from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database.base import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False, unique=True)
    slug = Column(String(150))
    imagem = Column(String(255), nullable=True)
    games = relationship("GameCategoria", back_populates="categoria")
    
