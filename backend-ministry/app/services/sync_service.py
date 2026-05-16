# app/services/sync_service.py
import logging
from typing import Any, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# Imports des modèles
from app.models.school import School
from app.models.sync_operation import SyncOperation, SyncStatus
from app.models.student import Student
from app.models.teacher import Teacher

# Imports des schémas
from app.schemas.sync import SyncPushRequest, SyncOperationDTO

# Import du Mapper que vous venez de créer
from app.mappers.school_to_ministry import get_mapper

logger = logging.getLogger(__name__)

# Dictionnaire pour mapper le type d'entité (string) vers la classe SQLAlchemy
ENTITY_MODELS = {
    "student": Student,
    "teacher": Teacher,
}

class SyncService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def process_push(self, request: SyncPushRequest) -> Dict[str, Any]:
        """
        Traite le lot d'opérations reçu de l'école.
        """
        accepted = 0
        rejected = 0
        conflicts = []
        
        logger.info(f"Réception push pour {request.school_code}: {len(request.operations)} opérations")
        
        # Vérifier que l'école existe 
    
        for op in request.operations:
            try:
               
                if await self._is_operation_processed(op.op_id):
                    logger.info(f"Opération déjà traitée (idempotence): {op.op_id}")
                    # On compte comme accepted car le résultat est déjà là, ou rejected selon votre choix
                    # Ici, on ignore silencieusement
                    continue

                # 2. Récupérer le bon Mapper
                mapper_func = get_mapper(op.entity)
                
                # 3. Traduire les données (Format École -> Format Ministère)
                mapped_data = mapper_func(op.payload)

                # 4. Appliquer la modification en base
                await self._apply_database_operation(op, mapped_data, request.school_id)

                # 5. Enregistrer le succès dans l'historique
                await self._log_operation(
                    op=op, 
                    school_id=request.school_id, 
                    status=SyncStatus.PROCESSED
                )
                accepted += 1

            except ValueError as e:
               
                logger.error(f"Erreur mapping pour {op.op_id}: {e}")
                await self._log_operation(op, request.school_id, SyncStatus.FAILED, error_msg=str(e))
                rejected += 1
                conflicts.append({"op_id": op.op_id, "error": str(e)})

            except Exception as e:
            
                logger.error(f"Erreur critique pour {op.op_id}: {e}")
                await self._log_operation(op, request.school_id, SyncStatus.FAILED, error_msg=str(e))
                rejected += 1
                conflicts.append({"op_id": op.op_id, "error": str(e)})
        
        # Commit pour tout sauvegarder
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Commit failed: {e}")
            raise e

        # Mettre à jour la date de dernière synchronisation de l'école
        await self._update_school_sync_status(request.school_id)

        return {
            "accepted": accepted,
            "rejected": rejected,
            "conflicts": conflicts,
            "server_version": datetime.utcnow().isoformat() + "Z"
        }

    async def _is_operation_processed(self, op_id: str) -> bool:
        """Vérifie si l'op_id existe déjà (Idempotence)."""
        result = await self.db.execute(
            select(SyncOperation).where(SyncOperation.operation_id == op_id)
        )
        return result.scalar_one_or_none() is not None

    async def _apply_database_operation(self, op: SyncOperationDTO, mapped_data: dict, school_id: str):
        """
        Applique réellement la modification (CREATE, UPDATE, DELETE) sur Student ou Teacher.
        """
        entity_type = op.entity.lower()
        if entity_type not in ENTITY_MODELS:
            raise ValueError(f"Entité non supportée: {op.entity}")

        ModelClass = ENTITY_MODELS[entity_type]

        if op.type == "create":
            # Création d'une nouvelle entité
            new_entity = ModelClass(
                id=op.entity_id,
                school_id=school_id,
                **mapped_data
            )
            self.db.add(new_entity)
            logger.info(f"Created {entity_type}: {op.entity_id}")

        elif op.type == "update":
            # Mise à jour
            result = await self.db.execute(select(ModelClass).where(ModelClass.id == op.entity_id))
            entity = result.scalar_one_or_none()
            
            if entity:
                for key, value in mapped_data.items():
                    if value is not None:
                        setattr(entity, key, value)
                logger.info(f"Updated {entity_type}: {op.entity_id}")
            else:
                raise ValueError(f"Update failed: {entity_type} {op.entity_id} not found")

        elif op.type == "delete":
            # Suppression
            result = await self.db.execute(select(ModelClass).where(ModelClass.id == op.entity_id))
            entity = result.scalar_one_or_none()
            
            if entity:
                await self.db.delete(entity)
                logger.info(f"Deleted {entity_type}: {op.entity_id}")
            else:
                raise ValueError(f"Delete failed: {entity_type} {op.entity_id} not found")

    async def _log_operation(self, op: SyncOperationDTO, school_id: str, status: SyncStatus, error_msg: str | None = None):
        """Enregistre l'historique de l'opération."""
        log_entry = SyncOperation(
            school_id=school_id,
            operation_id=op.op_id,
            entity_type=op.entity,
            entity_id=op.entity_id,
            operation_type=op.type,
            payload=op.payload,
            status=status,
            error_message=error_msg,
            processed_at=datetime.utcnow()
        )
        self.db.add(log_entry)

    async def _update_school_sync_status(self, school_id: str):
        """Met à jour le timestamp de dernière sync sur l'école."""
        result = await self.db.execute(select(School).where(School.id == school_id))
        school = result.scalar_one_or_none()
        if school:
            school.last_sync_at = datetime.utcnow()