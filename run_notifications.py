import asyncio
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from sqlalchemy import select
from app.database.session import AsyncSessionLocal, engine
from app.models.jogos_monitorados import JogosMonitorados
from app.services.notification_service import process_price_updates 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Iniciando job de verificação de preços...")
    
    async with AsyncSessionLocal() as db:
        try:
            logger.info("Buscando jogos monitorados...")
            
            result = await db.execute(select(JogosMonitorados.id))
            game_ids = [row[0] for row in result.all()]
            
            if game_ids:
                logger.info(f"Analisando {len(game_ids)} jogos...")
                count = await process_price_updates(game_ids, db)
                
                logger.info(f"Job finalizado. E-mails enviados: {count}")
            else:
                logger.info("Nenhum jogo encontrado no banco.")
                
        except Exception as e:
            logger.error(f"Erro crítico no job: {e}")
            raise e 

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())