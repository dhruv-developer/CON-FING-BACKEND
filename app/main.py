import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # read .env

from app.routers import behavior, anomaly

app = FastAPI(
    title="Cognitive Fingerprint AI",
    description="Behavioral intrusion forensics with GPT-3.5 explanations",
    version="1.0.0"
)

app.include_router(behavior.router, prefix="", tags=["Behavior"])
app.include_router(anomaly.router,  prefix="", tags=["Anomaly"])
