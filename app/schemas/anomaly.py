from pydantic import BaseModel
from typing import Dict

class AnalyzeAnomalyRequest(BaseModel):
    activity_id: str

class AnomalyResponse(BaseModel):
    anomaly_id: str
    user_id: str
    activity_id: str
    anomaly_score: float
    deviant_features: Dict[str, float]
    report: str
