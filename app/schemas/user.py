from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    nome: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class UserBasic(UserBase):
    id: UUID
    nome: str
    model_config = {"from_attributes": True}

class UserGoogleCreate(UserBase):
    google_id: str
    email: EmailStr
    avatar_url: str
    nome: str