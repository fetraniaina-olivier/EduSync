# seed_auth.py
"""
Crée une école et un utilisateur de test pour valider l'authentification.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models import School, User
from app.db.session import AsyncSessionLocal
from app.models.school import School
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select

async def seed():
    print(" Création des données de test...")
    
    async with AsyncSessionLocal() as session:
        # 1. Vérifier si l'école existe déjà
        result = await session.execute(select(School).where(School.code == "ECO-TEST-001"))
        school = result.scalar_one_or_none()
        
        if not school:
            school = School(
                code="ECO-TEST-001",
                name="École Pilote Paris",
                region="Île-de-France",
                city="Paris",
                is_active=True
            )
            session.add(school)
            await session.commit()
            await session.refresh(school)
            print(f"✅ École créée : {school.code} (ID: {school.id})")
        else:
            print(f"ℹ️ École déjà existante : {school.code}")

        # 2. Vérifier si l'utilisateur existe déjà
        result = await session.execute(select(User).where(User.username == "eco-test-001"))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                username="eco-test-001",
                hashed_password=get_password_hash("secret-eco-test-001"),
                role="school",
                school_id=school.id,
                is_active=True
            )
            session.add(user)
            await session.commit()
            print("✅ Utilisateur créé : eco-test-001")
        else:
            print("️ Utilisateur déjà existant : eco-test-001")

    print("\n📝 Credentials de test (à utiliser dans Swagger) :")
    print("   school_code : ECO-TEST-001")
    print("   secret      : secret-eco-test-001")
    print("\n🎉 Seed terminé !")

if __name__ == "__main__":
    asyncio.run(seed())