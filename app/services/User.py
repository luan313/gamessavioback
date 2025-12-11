from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select

class UserService:
    @staticmethod
    async def GetUserByEmail(email: str, db: AsyncSession) -> User:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()