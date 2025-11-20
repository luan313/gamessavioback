from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from app.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Plataforma(Base):
    __tablename__ = "plataforma"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100))

    games = relationship("GamePlataforma", back_populates="plataforma")