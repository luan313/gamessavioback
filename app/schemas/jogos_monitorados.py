from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class MonitoramentoBase(BaseModel):
    preco_alvo: float


class MonitoramentoCreate(MonitoramentoBase):
    preco_alvo: float
    game_id: UUID


class MonitoramentoUpdate(BaseModel):
    preco_alvo: Optional[float] = None


class MonitoramentoResponse(MonitoramentoBase):
    id: UUID
    user_id: UUID
    game_id: UUID
    created_at: datetime
    preco_alvo: float

    class Config:
        from_attributes = True

class MonitoramentoBasicResponse(MonitoramentoBase):
    id: UUID
    user_id: UUID
    game_id: UUID
    created_at: datetime
    preco_alvo: float

    class Config:
        from_attributes = True
