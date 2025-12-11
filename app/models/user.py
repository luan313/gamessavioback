from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    google_id = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)

    avaliacoes = relationship("Avaliacao", back_populates="user", cascade="all, delete")
    monitorados = relationship("JogosMonitorados", back_populates="user", cascade="all, delete")
