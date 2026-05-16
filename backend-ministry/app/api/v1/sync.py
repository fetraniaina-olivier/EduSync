# app/api/v1/sync.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta

from app.schemas.sync import SyncPushRequest
from app.services.sync_service import SyncService
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.school import School
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.sync_operation import SyncOperation, SyncStatus

router = APIRouter()

# ─────────────────────────────────────────────
# 🔴 EXISTANT : Endpoint PUSH (Envoi des données)
# ─────────────────────────────────────────────
@router.post("/push")
async def push_data(
    request: SyncPushRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reçoit les données de synchronisation depuis une école."""
    # Vérification basique que l'utilisateur correspond à l'école envoyée
    if current_user.school_id != request.school_id:
        raise HTTPException(status_code=403, detail="Non autorisé pour cette école")

    service = SyncService(db)
    result = await service.process_push(request)
    return result

# ─────────────────────────────────────────────
# 🟢 NOUVEAU : Endpoints GET (Pour le Dashboard)
# ─────────────────────────────────────────────

@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retourne les statistiques globales pour le dashboard."""
    today = datetime.utcnow() - timedelta(days=1)
    
    # Comptages parallèles
    schools_q = await db.execute(select(func.count(School.id)))
    students_q = await db.execute(select(func.count(Student.id)))
    teachers_q = await db.execute(select(func.count(Teacher.id)))
    syncs_q = await db.execute(select(func.count(SyncOperation.id)).where(SyncOperation.processed_at >= today))
    
    return {
        "schools": schools_q.scalar() or 0,
        "students": students_q.scalar() or 0,
        "teachers": teachers_q.scalar() or 0,
        "syncs_today": syncs_q.scalar() or 0
    }

@router.get("/schools")
async def get_schools_list(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retourne la liste des écoles avec le nombre d'étudiants."""
    result = await db.execute(select(School).order_by(School.name))
    schools = result.scalars().all()
    
    output = []
    for s in schools:
        # Compte les étudiants pour chaque école
        stu_count = await db.execute(select(func.count(Student.id)).where(Student.school_id == str(s.id)))
        output.append({
            "id": str(s.id),
            "code": s.code,
            "name": s.name,
            "region": s.region or "N/A",
            "students": stu_count.scalar() or 0,
            "status": "actif" if s.is_active else "inactif",
            "last_sync": s.last_sync_at.strftime("%H:%M") if s.last_sync_at else "Jamais"
        })
    return output

@router.get("/activities")
async def get_recent_activities(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retourne les 5 dernières opérations de sync."""
    q = select(SyncOperation).order_by(desc(SyncOperation.processed_at)).limit(5)
    result = await db.execute(q)
    ops = result.scalars().all()
    
    return [{
        "type": op.entity_type,
        "count": 1, 
        "source": "École", 
        "time": op.processed_at.strftime("%H:%M") if op.processed_at else "Récemment",
        "status": "success" if op.status == SyncStatus.PROCESSED else "warning"
    } for op in ops]
# ─────────────────────────────────────────────
#  NOUVEAU : Détail des étudiants par école
# ─────────────────────────────────────────────
@router.get("/schools/{school_id}/students")
async def get_school_students(
    school_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retourne la liste complète des étudiants d'une école spécifique."""
    from sqlalchemy import select
    
    result = await db.execute(
        select(Student)
        .where(Student.school_id == school_id)
        .order_by(Student.last_name, Student.first_name)
    )
    students = result.scalars().all()
    
    return [
        {
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            # ✅ Correction : utiliser str() pour les dates
            "birth_date": str(s.birth_date) if s.birth_date else None,
            "enrollment_date": str(s.enrollment_date) if s.enrollment_date else None,
           
        }
        for s in students
    ]