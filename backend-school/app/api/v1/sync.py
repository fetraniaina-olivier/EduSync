from fastapi import APIRouter, HTTPException
from app.services.sync_service import push_to_ministry

router = APIRouter()

@router.post("/trigger")
async def trigger_sync():
    try:
        result = await push_to_ministry()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))