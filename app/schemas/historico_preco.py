from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class HistoricoPrecoBase(BaseModel):
    preco: float
    loja: Optional[str] = None


class HistoricoPrecoCreate(HistoricoPrecoBase):
    game_id: UUID


class HistoricoPrecoResponse(HistoricoPrecoBase):
    id: UUID
    game_id: UUID
    data_coleta: datetime

    class Config:
        from_attributes = True
