# app/schemas/auth.py
"""
Schémas Pydantic pour l'authentification.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """Réponse de login avec token d'accès"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # secondes

class TokenData(BaseModel):
    """Données décodées d'un token JWT"""
    username: Optional[str] = None
    role: Optional[str] = None
    school_id: Optional[str] = None

class SchoolLoginRequest(BaseModel):
    """Requête de login pour une école"""
    school_code: str = Field(..., min_length=3, description="Code de l'école")
    secret: str = Field(..., min_length=8, description="Secret d'authentification")
    
    class Config:
        json_schema_extra = {
            "example": {
                "school_code": "ECO-PARIS-001",
                "secret": "mon-secret-securise-123"
            }
        }

class UserCreate(BaseModel):
    """Création d'un utilisateur (admin uniquement)"""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    role: str = Field(default="school")
    school_id: Optional[str] = None

class UserResponse(BaseModel):
    """Informations utilisateur publiques"""
    username: str
    role: str
    school_id: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True