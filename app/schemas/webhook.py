from pydantic import BaseModel
from typing import List
from uuid import UUID

class PriceUpdatePayload(BaseModel):
    game_ids: List[UUID]
