# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1️⃣ Créer le moteur de base de données
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 2️⃣ Factory de sessions asynchrones
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3️⃣ CORRECTION CRITIQUE : Base est une classe dont on hérite (SQLAlchemy 2.0)
# ⚠️ NE PAS ÉCRIRE: Base = DeclarativeBase()  ← C'EST ÇA QUI PROVOQUE L'ERREUR
class Base(DeclarativeBase):
    pass