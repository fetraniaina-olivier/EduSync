# seed_auth.py
"""
Script pour créer des utilisateurs de test.
À exécuter une fois après avoir initialisé la DB.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.user import User
from app.models.school import School
from app.core.security import get_password_hash

async def seed_auth_data():
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # 1. Créer une école de test si elle n'existe pas
        school = School(
            code="ECO-TEST-001",
            name="École Test Paris",
            region="Île-de-France",
            city="Paris",
            is_active=True
        )
        
        session.add(school)
        await session.commit()
        await session.refresh(school)
        print(f"✅ École créée: {school.code} (ID: {school.id})")
        
        # 2. Créer un utilisateur pour cette école
        user = User(
            username="eco-test-001",
            hashed_password=get_password_hash("secret-eco-test-001"),
            role="school",
            school_id=school.id,
            is_active=True
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"✅ Utilisateur créé: {user.username}")
        
        print("\n📝 Credentials de test:")
        print(f"   school_code: ECO-TEST-001")
        print(f"   secret: secret-eco-test-001")
        print(f"   username: eco-test-001")
        print(f"   password: secret-eco-test-001")
    
    await engine.dispose()
    print("\n🎉 Seed terminé avec succès !")

if __name__ == "__main__":
    asyncio.run(seed_auth_data())