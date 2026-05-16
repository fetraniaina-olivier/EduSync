# test_db.py
import asyncio
import sys
from pathlib import Path
from sqlalchemy import text  # ✅ IMPORT CRITIQUE
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

sys.path.insert(0, str(Path(__file__).parent))

async def test_connection():
    print("Test de connexion à PostgreSQL...")
    
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        async with engine.connect() as conn:

            # Envelopper la requête brute avec text()
            result = await conn.execute(text("SELECT version()"))
            pg_version = result.scalar()
            print("✅ Connexion réussie !")
            print(f"📦 PostgreSQL version: {pg_version}")
            print(f"🗄️ Base de données: {settings.DB_NAME}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ Échec de connexion : {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_connection())