from fastapi import FastAPI
from app.routers import (
    auth_router,
    backoffice,
    avaliacao_router,
    monitoramento_router,
    game_router
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI(title="Letterboxd de Jogos")

origins = [
    "http://localhost:3000",        
    "http://127.0.0.1:3000",
    "http://localhost:5173",        
    "https://seu-dominio.com"      
]
add_pagination(app)

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
app.include_router(monitoramento_router.router, tags=["monitoramento"])
app.include_router(game_router.router, tags=["game"])