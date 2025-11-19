from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MonitoramentoBase(BaseModel):
    preco_a_pagar: float


class MonitoramentoCreate(MonitoramentoBase):
    game_id: UUID


class MonitoramentoResponse(MonitoramentoBase):
    id: UUID
    user_id: UUID
    game_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
