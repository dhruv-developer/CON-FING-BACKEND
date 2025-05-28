from app.database import db
from bson import ObjectId

async def insert_activity(activity: dict):
    return await db.activities.insert_one(activity)

async def get_activity(activity_id: str):
    return await db.activities.find_one({"_id": ObjectId(activity_id)})

async def get_user_activities(user_id: str, exclude_id: str = None):
    query = {"user_id": user_id}
    if exclude_id:
        query["_id"] = {"$ne": ObjectId(exclude_id)}
    return await db.activities.find(query).to_list(length=None)

async def insert_anomaly(anomaly: dict):
    return await db.anomalies.insert_one(anomaly)

async def get_anomalies():
    return await db.anomalies.find().to_list(length=None)
