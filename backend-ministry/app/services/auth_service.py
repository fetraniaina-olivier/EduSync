# app/services/auth_service.py
"""
Service d'authentification et de gestion des utilisateurs.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.school import School
from app.schemas.auth import SchoolLoginRequest
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_school(self, login_data: SchoolLoginRequest) -> User | None:
        """
        Authentifie une école par son code et son secret.
        
        En production, le "secret" serait un mot de passe hashé en base.
        Pour le dev, on utilise une logique simplifiée.
        """
        # Chercher l'école par son code
        result = await self.db.execute(
            select(School).where(School.code == login_data.school_code)
        )
        school = result.scalar_one_or_none()
        
        if not school or not school.is_active:
            return None
        
        # Chercher l'utilisateur lié à cette école
        result = await self.db.execute(
            select(User).where(User.school_id == school.id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return None
        
        # Vérifier le mot de passe (ou secret)
        # Pour le dev : on accepte si le secret correspond à un pattern simple
        # En prod : utiliser verify_password(login_data.secret, user.hashed_password)
        if login_data.secret == f"secret-{school.code.lower()}":  # DEV ONLY
            return user
        
        return None
    
    async def create_user(self, username: str, password: str, role: str, school_id: str | None = None) -> User:
        """Crée un nouvel utilisateur avec mot de passe hashé"""
        hashed_password = get_password_hash(password)
        
        user = User(
            username=username,
            hashed_password=hashed_password,
            role=role,
            school_id=school_id,
            is_active=True
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    def generate_token(self, user: User) -> str:
        """Génère un token JWT pour un utilisateur"""
        token_data = {
            "sub": user.username,  # subject
            "role": user.role,
            "school_id": user.school_id
        }
        
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(token_data, expires_delta)