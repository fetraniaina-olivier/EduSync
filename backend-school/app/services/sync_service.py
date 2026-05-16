# backend-school/app/services/sync_service.py
import httpx
import logging
from datetime import datetime
from sqlalchemy import select, update
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.student import Student

logger = logging.getLogger(__name__)

async def push_to_ministry():
    """Synchronise les étudiants non synchronisés vers le Ministère."""
    async with AsyncSessionLocal() as db:
        # 1. Récupérer les étudiants en attente
        result = await db.execute(select(Student).where(Student.is_synced == False))
        unsynced_students = result.scalars().all()

        if not unsynced_students:
            return {"message": "Aucune donnée à synchroniser", "accepted": 0}

        # 2. Préparer le payload EXACT comme dans le test manuel
        operations = []
        for stu in unsynced_students:
            operations.append({
                "op_id": f"op-{stu.id}-{int(datetime.utcnow().timestamp())}",
                "type": "create",
                "entity": "student",
                "entity_id": stu.id,
                "payload": {
                    "first_name": stu.first_name,
                    "last_name": stu.last_name,
                    "birth_date": stu.birth_date.isoformat(),
                    "enrollment_date": stu.enrollment_date.isoformat()
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })

        payload = {
            "school_id": settings.SCHOOL_ID,
            "school_code": settings.SCHOOL_CODE,
            "client_version": datetime.utcnow().isoformat() + "Z",
            "operations": operations
        }

       # Remplacez la section try/except par celle-ci (avec print) :

        try:
            # 🔍 DEBUG AFFICHAGE GARANTI
            base_url = settings.MINISTRY_API_URL.rstrip('/')
            login_url = f"{base_url}/auth/login/school"
            push_url = f"{base_url}/sync/push"
            
            print(f"\n{'='*60}")
            print(f"🔗 DEBUG: MINISTRY_API_URL from .env = {settings.MINISTRY_API_URL}")
            print(f"🔗 DEBUG: Login URL appelée = {login_url}")
            print(f"🔗 DEBUG: Push URL appelée = {push_url}")
            print(f"{'='*60}\n")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 3. Authentification
                print(f"🔑 Envoi POST vers: {login_url}")
                
                login_resp = await client.post(
                    login_url,
                    json={"school_code": settings.SCHOOL_CODE, "secret": settings.SCHOOL_SECRET}
                )
                
                print(f"🔑 Réponse: {login_resp.status_code} - {login_resp.text}\n")
                
                if login_resp.status_code == 404:
                    print(f"❌ ERREUR: L'endpoint n'existe pas à cette URL!")
                    print(f"💡 Essayez dans votre navigateur: {login_url}")
                    raise Exception(f"Endpoint introuvable: {login_url}")
                
                login_resp.raise_for_status()
                token = login_resp.json()["access_token"]

                # 4. Push
                print(f"📤 Envoi POST vers: {push_url}")
                push_resp = await client.post(
                    push_url,
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                print(f"📤 Réponse: {push_resp.status_code} - {push_resp.text}\n")
                
                if push_resp.status_code != 200:
                    raise Exception(f"Échec push: {push_resp.text}")

                result_data = push_resp.json()

                # 5. Update local
                ids_to_sync = [s.id for s in unsynced_students]
                await db.execute(update(Student).where(Student.id.in_(ids_to_sync)).values(is_synced=True))
                await db.commit()

                print(f"🎉 SYNCHRONISATION RÉUSSIE!\n")
                return result_data

        except Exception as e:
            await db.rollback()
            print(f"💥 ERREUR FATALE: {str(e)}\n")
            raise