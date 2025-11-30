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

class GameCategoriaAssociation(BaseModel):
    categoria: CategoriaResponse
    class Config:
        from_attributes = True

class GameBasic(BaseModel):
    id: UUID
    nome: str
   
    class Config:
        from_attributes = True

class GameExpose(BaseModel):
    id: UUID
    imagem_capa: Optional[str] = None
    nome: str
    categorias: List[GameCategoriaAssociation] = []
    updated_at: Optional[datetime] = None
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    hype: int = 0

    class Config:
        from_attributes = True

class GameCreate(GameBase):
    rawg_id: Optional[int] = None
    categorias_ids: List[UUID] = []
    plataformas_ids: List[UUID] = []
    


class GamePlataformaAssociation(BaseModel):
    plataforma: PlataformaResponse
    class Config:
        from_attributes = True

class GameResponse(GameBase):
    id: UUID
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    isthereanydeal_id: Optional[str] = None
    deal_url: Optional[str] = None      
    store_name: Optional[str] = None    
    imagem_capa: Optional[str] = None
    hype: int = 0
    
    updated_at: Optional[datetime] = None
    
    categorias: List[GameCategoriaAssociation] = []
    plataformas: List[GamePlataformaAssociation] = []

    class Config:
        from_attributes = True



class GameForMonitoramento(BaseModel):
    id: UUID
    nome: str
    imagem_capa: Optional[str] = None
    deal_url: Optional[str] = None
    last_price: Optional[float] = None

    class Config:
        from_attributes = True
        
class TopHypedGamesResponse(GameBase):
    id: UUID
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    isthereanydeal_id: Optional[str] = None
    deal_url: Optional[str] = None      
    store_name: Optional[str] = None    
    imagem_capa: Optional[str] = None
    hype: int = 0
    
    updated_at: Optional[datetime] = None
    

    class Config:
        from_attributes = True

class SearchGameResponse(GameBase):
    id: UUID
    nota_media: Optional[float] = None
    last_price: Optional[float] = None
    isthereanydeal_id: Optional[str] = None
    deal_url: Optional[str] = None      
    store_name: Optional[str] = None    
    imagem_capa: Optional[str] = None
    
    

    class Config:
        from_attributes = True