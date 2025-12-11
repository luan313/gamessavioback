
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum
from sqlalchemy import DateTime, Boolean
from app.database.base import Base

class VerificationType(str, Enum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"

class EmailVerifications(Base):
    __tablename__ = "email_verifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    code = Column(String(6), nullable=False)
    verification_type = Column(SqlEnum(VerificationType), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    expires_at = Column(DateTime, nullable=False, default=datetime.now() + timedelta(minutes=15))
    used = Column(Boolean, nullable=False, default=False)
    
    user = relationship("User", back_populates="email_verifications")

    