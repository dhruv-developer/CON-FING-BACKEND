import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME      = os.getenv("DB_NAME", "cognitive_fingerprint")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI must be set in .env")

client = AsyncIOMotorClient(MONGODB_URI)
db     = client[DB_NAME]
