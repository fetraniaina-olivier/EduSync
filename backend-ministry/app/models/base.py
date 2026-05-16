# app/models/base.py
"""
Classe de base pour tous les modèles SQLAlchemy 2.0.
"""
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer
from datetime import datetime
import uuid

@as_declarative()
class Base:
    """Classe de base avec champs communs à tous les modèles."""
    
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # ⚠️ SQLAlchemy 2.0 : utiliser Mapped[] pour les colonnes mappées
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)