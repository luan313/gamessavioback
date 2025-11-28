import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from app.routers import (
    auth,
    backoffice,
    avaliacao,
    monitoramento,
    game,
    categoria,
    webhook,
    user
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import logging
from redis import asyncio as aioredis
from app.core.config import settings    
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@asynccontextmanager
async def lifespan(app: FastAPI):
   redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    
   FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
   yield
    
   await redis_client.close()


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Letterboxd de Jogos", 
    lifespan=lifespan)

origins = [
    "http://localhost:3000",        
    "http://127.0.0.1:3000",
    "https://gamessaviofront.vercel.app",
    "http://localhost:5173",        
]
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],           
)


app.include_router(auth.router, tags=["Auth"])
app.include_router(backoffice.router, tags=["backoffice"])
app.include_router(avaliacao.router, tags=["avaliação"])
app.include_router(monitoramento.router, tags=["monitoramento"])
app.include_router(game.router, tags=["game"])
app.include_router(categoria.router, tags=["categoria"])
app.include_router(webhook.router, tags=["webhook"])
app.include_router(user.router, tags=["user"])



docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "_build", "html")

@app.get("/")
def root():
    return {"message": "GamesSavio API", "Swagger": "/docs", "sphinx_docs": "/documentation"}

if os.path.exists(docs_path):
    app.mount("/documentation", StaticFiles(directory=docs_path, html=True), name="docs")
else:
    logging.warning(f"Directory {docs_path} does not exist. Documentation will not be served.")