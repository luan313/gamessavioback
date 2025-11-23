from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CategoriaResponse(BaseModel):
    id: UUID
    nome: str
    slug: Optional[str] = None

    class Config:
        from_attributes = True

class PlataformaResponse(BaseModel):
    id: UUID
    nome: str
    slug: Optional[str] = None

    class Config:
        from_attributes = True