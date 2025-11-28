from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
from app.schemas.user import UserBasic
from app.schemas.game import GameBasic

class AvaliacaoBase(BaseModel):
    comentario: Optional[str] = None
    nota: int = Field(..., ge=0, le=10, description="Nota de 0 a 10")


class AvaliacaoCreate(AvaliacaoBase):
    game_id: UUID4


class AvaliacaoUpdate(BaseModel):
    comentario: Optional[str] = None
    nota: Optional[int] = Field(None, ge=0, le=10)


class AvaliacaoResponse(AvaliacaoBase):
    id: UUID4
    user_id: UUID4
    game_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True 

class AvaliacaoDetailedResponse(AvaliacaoBase):
    id: UUID4
    user: UserBasic
    created_at: datetime

    class Config:
        from_attributes = True

class AvaliacaoBasicResponse(AvaliacaoBase):
    id: UUID4
    user: UserBasic
    game: GameBasic
    created_at: datetime

    class Config:
        from_attributes = True 