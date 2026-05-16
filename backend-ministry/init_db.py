# init_db.py
"""
Script d'initialisation de la base de données.

IMPORTANT : Doit importer TOUS les modèles avant create_all()
"""
import asyncio
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from app.models.base import Base

# Importer TOUS les modèles pour les enregistrer dans SQLAlchemy
from app.models import school      # noqa: F401
from app.models import user        # noqa: F401
from app.models import sync_operation  # noqa: F401

sys.path.insert(0, str(Path(__file__).parent))

async def init_db():
    print("🗄️ Initialisation de la base de données...")
    
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
    # echo=True pour voir les requêtes SQL créées (utile pour déboguer)
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    try:
        async with engine.begin() as conn:
            # Maintenant que tous les modèles sont importés, create_all() les voit tous
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables créées avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        sys.exit(1)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())