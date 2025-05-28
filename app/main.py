import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # read .env

from app.routers import behavior, anomaly

app = FastAPI(
    title="Cognitive Fingerprint AI",
    description="Behavioral intrusion forensics with GPT-3.5 explanations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(behavior.router, prefix="", tags=["Behavior"])
app.include_router(anomaly.router,  prefix="", tags=["Anomaly"])
