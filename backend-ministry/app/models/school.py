# app/models/school.py
"""
Modèle SQLAlchemy 2.0 pour les établissements scolaires.
"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class School(Base):
    """
    Représente un établissement scolaire dans le référentiel ministère.
    """
    __tablename__ = "schools"
    
    # SQLAlchemy 2.0 : Mapped[type] = mapped_column(...)
    
    # Identifiants
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Localisation
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    
    # Contact
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    
    # Statut
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # ==========================================
    # ️ RELATIONS
    # ==========================================
    
    # 1. Relation avec les opérations de sync (existant)
    sync_operations: Mapped[list["SyncOperation"]] = relationship(
        "SyncOperation", 
        back_populates="school", 
        cascade="all, delete-orphan"
    )
    
    # 2. Relation avec les étudiants

    students: Mapped[list["Student"]] = relationship(
        "Student", 
        back_populates="school", 
        cascade="all, delete-orphan"
    )
    
    # 3. Relation avec les enseignants (NOUVEAU)
    teachers: Mapped[list["Teacher"]] = relationship(
        "Teacher", 
        back_populates="school", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<School(code='{self.code}', name='{self.name}')>"