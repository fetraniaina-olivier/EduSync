# app/schemas/sync.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# =============================================================================
# ENUMS
# =============================================================================
class SyncEntityType(str, Enum):
    """Types d'entités synchronisables"""
    STUDENT = "student"
    TEACHER = "teacher"
    ATTENDANCE = "attendance"
    GRADE = "grade"

class SyncOperationType(str, Enum):
    """Types d'opérations de sync"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class SyncStatus(str, Enum):
    """Statuts de traitement d'une opération"""
    PENDING = "pending"
    PROCESSED = "processed"
    CONFLICT = "conflict"
    FAILED = "failed"

# =============================================================================
# DTOs POUR LES OPÉRATIONS DE SYNC
# =============================================================================
class SyncOperationDTO(BaseModel):
    """
    Représente une opération individuelle envoyée par une école.
    """
    op_id: str = Field(..., description="ID unique de l'opération (généré par l'école)")
    type: SyncOperationType = Field(..., description="Type d'opération: create/update/delete")
    entity: SyncEntityType = Field(..., description="Type d'entité: student/teacher/etc.")
    entity_id: str = Field(..., description="ID de l'entité cible")
    payload: Dict[str, Any] = Field(..., description="Données complètes de l'entité")
    timestamp: Optional[datetime] = Field(default=None, description="Horodatage de l'opération")

    class Config:
        json_schema_extra = {
            "example": {
                "op_id": "op-uuid-123",
                "type": "create",
                "entity": "student",
                "entity_id": "student-uuid-456",
                "payload": {"name": "Jean Dupont", "grade": "5ème", "enrollment_date": "2024-09-01"},
                "timestamp": "2024-04-20T10:30:00Z"
            }
        }

# =============================================================================
# REQUÊTES ENTRANTES (REQUEST)
# =============================================================================
class SyncPushRequest(BaseModel):
    """
    Payload complet envoyé par une école via POST /sync/push
    """
    school_id: str = Field(..., description="ID unique de l'école (UUID)")
    school_code: Optional[str] = Field(None, description="Code métier de l'école (ex: ECO-001)")
    client_version: str = Field(..., description="Version/dernière sync connue par le client (ISO datetime)")
    operations: List[SyncOperationDTO] = Field(..., min_items=1, max_items=1000, description="Liste des opérations à appliquer")

    class Config:
        json_schema_extra = {
            "example": {
                "school_id": "school-uuid-789",
                "school_code": "ECO-PARIS-01",
                "client_version": "2024-04-20T09:00:00Z",
                "operations": [
                    {
                        "op_id": "op-uuid-1",
                        "type": "create",
                        "entity": "student",
                        "entity_id": "student-uuid-abc",
                        "payload": {"name": "Marie Curie", "grade": "Terminale"},
                        "timestamp": "2024-04-20T10:00:00Z"
                    }
                ]
            }
        }

class SyncPullRequest(BaseModel):
    """
    Payload pour récupérer les mises à jour depuis le ministère
    """
    school_id: str = Field(..., description="ID de l'école")
    client_version: str = Field(..., description="Dernière version sync connue")
    entity_types: Optional[List[SyncEntityType]] = Field(default=None, description="Filtrer par types d'entités")

# =============================================================================
# RÉPONSES SORTANTES (RESPONSE)
# =============================================================================
class SyncConflictDTO(BaseModel):
    """
    Représente un conflit détecté entre les données école et ministère
    """
    conflict_id: str = Field(..., description="ID unique du conflit")
    operation_id: str = Field(..., description="ID de l'opération qui a causé le conflit")
    entity_type: str = Field(..., description="Type d'entité concernée")
    entity_id: str = Field(..., description="ID de l'entité concernée")
    school_value: Dict[str, Any] = Field(..., description="Valeur proposée par l'école")
    ministry_value: Dict[str, Any] = Field(..., description="Valeur actuelle au ministère")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="Date de détection")
    status: SyncStatus = Field(default=SyncStatus.CONFLICT, description="Statut du conflit")

class SyncResponse(BaseModel):
    """
    Réponse standard après traitement d'un push/pull
    """
    accepted: int = Field(..., description="Nombre d'opérations acceptées")
    rejected: int = Field(..., description="Nombre d'opérations rejetées")
    conflicts: List[SyncConflictDTO] = Field(default_factory=list, description="Liste des conflits détectés")
    server_version: str = Field(..., description="Nouvelle version serveur (à utiliser pour le prochain pull)")
    next_sync_url: Optional[str] = Field(default=None, description="URL pour récupérer les mises à jour")

    class Config:
        json_schema_extra = {
            "example": {
                "accepted": 45,
                "rejected": 2,
                "conflicts": [],
                "server_version": "2024-04-20T10:35:00Z",
                "next_sync_url": "/api/v1/sync/pull?since=2024-04-20T10:35:00Z"
            }
        }

class HealthResponse(BaseModel):
    """Réponse pour l'endpoint de santé"""
    status: str = "ok"
    service: str = "ministry-backend"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"