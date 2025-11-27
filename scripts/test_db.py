import asyncio
import sys
import ssl
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# --- 1. CONFIGURAÇÃO ---
# Cole sua URL aqui DENTRO DAS ASPAS para testar.
# IMPORTANTE:
# 1. Comece com "postgresql+asyncpg://"
# 2. NÃO coloque "?sslmode=..." no final. Pare no nome do banco.
DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_C3mVMzr6OABY@ep-super-morning-a4drmew2-pooler.us-east-1.aws.neon.tech/neondb"

# --- 2. FIX DO WINDOWS (Obrigatório) ---
if sys.platform.startswith("win"):
    print("🔧 Aplicando fix do Windows SelectorEventLoop...")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- 3. FIX DE SSL (Obrigatório para Nuvem) ---
# Cria um contexto que aceita criptografia mas ignora erros de certificado
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def test_connection():
    print(f"📡 Tentando conectar em: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'URL INVÁLIDA'}...")
    
    try:
        # Cria a engine com o SSL permissivo injetado
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            connect_args={"ssl": ssl_context} 
        )

        # Tenta conectar e rodar uma query simples
        async with engine.connect() as conn:
            print("⏳ Conexão estabelecida! Rodando query de teste...")
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("\n✅ SUCESSO! O Banco respondeu:")
            print(f"   {version}")
            
    except Exception as e:
        print("\n❌ ERRO DE CONEXÃO:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    if "SEU_USUARIO" in DATABASE_URL:
        print("⚠️  ERRO: Você esqueceu de editar a variável DATABASE_URL na linha 12!")
    else:
        asyncio.run(test_connection())