import sys
from pathlib import Path
import os
import asyncio

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

# Mock environment variables
os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:pass@localhost/dbname"

async def verify():
    try:
        from app.services.categoria import CategoriaService
        print("Successfully imported CategoriaService")
        
        if hasattr(CategoriaService, 'get_categorias_com_quantidade_jogos'):
            print("CategoriaService has 'get_categorias_com_quantidade_jogos' method")
            
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
