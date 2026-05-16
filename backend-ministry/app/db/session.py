# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

# Construction de l'URL de connexion PostgreSQL
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Création du moteur asynchrone
engine = create_async_engine(DATABASE_URL, echo=settings.DEBUG, future=True)

# Factory de sessions async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

#Dépendance FastAPI pour injecter la DB dans les routes
async def get_db() -> AsyncSession:
    """
    Dépendance FastAPI qui fournit une session DB.
    Usage: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()