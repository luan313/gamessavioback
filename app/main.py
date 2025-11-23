from fastapi import FastAPI
from app.routers import (
    auth_router,
    backoffice,
    avaliacao_router,
)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",        
    "http://127.0.0.1:3000",
    "http://localhost:5173",        
    "https://seu-dominio.com"      
]

app = FastAPI(title="Letterboxd de Jogos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],           
)


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(backoffice.router, tags=["backoffice"])
app.include_router(avaliacao_router.router, tags=["avaliação"])