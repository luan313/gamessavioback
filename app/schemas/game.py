from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class GameBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class GameCreate(GameBase):
    categorias: List[UUID] = []


class GameResponse(GameBase):
    id: UUID
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    isthereanydeal_id: Optional[str] = None

    class Config:
        from_attributes = True
