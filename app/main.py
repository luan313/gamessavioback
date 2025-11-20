from fastapi import FastAPI
from app.routers import (
    auth_router,
    backoffice,
    user_router,
    game_router,
    categoria_router,
    avaliacao_router,
    monitoramento_router,
)

app = FastAPI(title="Letterboxd de Jogos")
app.include_router(auth_router.router, tags=["Auth"])
app.include_router(backoffice.router, tags=["backoffice"])
app.include_router(avaliacao_router.router, tags=["avaliação"])