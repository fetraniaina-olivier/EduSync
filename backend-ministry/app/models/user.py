# app/models/user.py
"""
Modèle pour les utilisateurs (écoles) avec credentials d'authentification.
"""
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class User(Base):
    """
    Représente un utilisateur système (école ou admin ministère).
    """
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Lien vers une école si c'est un compte école
    school_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("schools.id"), nullable=True)
    
    # Rôles: "school", "ministry_admin", "super_admin"
    role: Mapped[str] = mapped_column(String(20), default="school", nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relations
    school = relationship("School", backref="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"