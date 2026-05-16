# app/api/v1/auth.py
"""
Endpoints d'authentification pour les écoles et administrateurs.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SchoolLoginRequest, Token, UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/login/school", response_model=Token)
async def school_login(
    login_data: SchoolLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authentifie une école et retourne un token JWT.
    
    Le token doit être inclus dans les requêtes suivantes via le header :
    `Authorization: Bearer <token>`
    """
    auth_service = AuthService(db)
    
    # Authentifier l'école
    user = await auth_service.authenticate_school(login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect school code or secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Générer le token
    access_token = auth_service.generate_token(user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=1800  # 30 minutes
    )

@router.post("/login/admin", response_model=Token)
async def admin_login(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Authentifie un administrateur du ministère.
    (Endpoint simplifié pour le dev - à sécuriser en prod)
    """
    # TODO: Implémenter la logique admin complète
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Retourne les informations de l'utilisateur authentifié"""
    return current_user

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("super_admin"))
):
    """
    Crée un nouvel utilisateur (réservé aux super admins).
    """
    auth_service = AuthService(db)
    
    # Vérifier si l'utilisateur existe déjà
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Créer l'utilisateur
    new_user = await auth_service.create_user(
        username=user_data.username,
        password=user_data.password,
        role=user_data.role,
        school_id=user_data.school_id
    )
    
    return new_user