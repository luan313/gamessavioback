from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


class AvaliacaoCreate(AvaliacaoBase):
    game_id: UUID


class AvaliacaoResponse(AvaliacaoBase):
    id: UUID
    user_id: UUID
    game_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
