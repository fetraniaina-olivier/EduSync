# app/models/sync_operation.py
"""
Modèle pour tracer les opérations de synchronisation (SQLAlchemy 2.0).
"""
from datetime import datetime 
from sqlalchemy import String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from app.models.base import Base

class SyncStatus(str, enum.Enum):
    """Statuts possibles d'une opération de sync."""
    PENDING = "pending"
    PROCESSED = "processed"
    CONFLICT = "conflict"
    FAILED = "failed"

class SyncOperation(Base):
    """
    Enregistre chaque opération de synchronisation reçue d'une école.
    """
    __tablename__ = "sync_operations"
    
    # Clés étrangères
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    
    # Identifiant unique de l'opération (généré par l'école)
    operation_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)
    
    # Type d'entité et d'opération
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Données
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    previous_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    # Statut
    status: Mapped[SyncStatus] = mapped_column(SQLEnum(SyncStatus), default=SyncStatus.PENDING, index=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relations
    school: Mapped["School"] = relationship("School", back_populates="sync_operations")
    
    def __repr__(self):
        return f"<SyncOperation(op_id='{self.operation_id}', status='{self.status}')>"