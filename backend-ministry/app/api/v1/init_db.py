# init_db.py
"""
Script d'initialisation de la base de données.
Crée toutes les tables définies dans les modèles SQLAlchemy.
"""
import asyncio
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.config import settings

# Ajoute le dossier courant au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

async def init_db():
    print("️ Initialisation de la base de données...")
    
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Crée toutes les tables (School, SyncOperation, User, etc.)
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables créées avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        sys.exit(1)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())