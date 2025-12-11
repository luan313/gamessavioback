from app.utils import tools
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models.email_verifications import EmailVerifications
from app.models.email_verifications import VerificationType

async def create_reset_coode(user_id: UUID, db: AsyncSession, verification_type: VerificationType, time: int = 15):
    code = tools.gerar_codigo()
    expires_at = datetime.now() + timedelta(minutes=time)

    verification = EmailVerifications(
        user_id=user_id, 
        code=code, 
        expires_at=expires_at, 
        verification_type=verification_type)

    db.add(verification)
    await db.commit()
    return verification