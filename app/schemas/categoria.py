from pydantic import BaseModel
from uuid import UUID


class CategoriaBase(BaseModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaResponse(CategoriaBase):
    id: UUID

    class Config:
        from_attributes = True


class CategoriaComJogos(BaseModel):
    id: UUID
    nome: str
    quantidade_jogos: int
    imagem: str

    class Config:
        from_attributes = True
