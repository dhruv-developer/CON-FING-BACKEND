from fastapi import APIRouter
from app.schemas.behavior import BehaviorLog
from app.services.db import insert_activity

router = APIRouter()

@router.post("/log_activity", summary="Log a user behavior event")
async def log_activity(log: BehaviorLog):
    # Exclude fields with value None (especially _id)
    data = log.dict(by_alias=True, exclude_none=True)
    result = await insert_activity(data)
    return {"activity_id": str(result.inserted_id)}
