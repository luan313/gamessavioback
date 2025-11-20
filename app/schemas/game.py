from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import date, datetime
from app.schemas.plataforma import PlataformaResponse
from app.schemas.categoria import CategoriaResponse

class GameBase(BaseModel):
    nome: str
    slug: Optional[str] = None
    descricao: Optional[str] = None
    imagem_capa: Optional[str] = None
    data_lancamento: Optional[date] = None
    metacritic: Optional[int] = None

class GameCreate(GameBase):
    rawg_id: Optional[int] = None
    categorias_ids: List[UUID] = []
    plataformas_ids: List[UUID] = []
    
class GameCategoriaAssociation(BaseModel):
    categoria: CategoriaResponse
    class Config:
        from_attributes = True

class GamePlataformaAssociation(BaseModel):
    plataforma: PlataformaResponse
    class Config:
        from_attributes = True


class GameResponse(GameBase):
    id: UUID
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    isthereanydeal_id: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    categorias: List[GameCategoriaAssociation] = []
    plataformas: List[GamePlataformaAssociation] = []

    class Config:
        from_attributes = True
        
