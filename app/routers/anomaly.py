import numpy as np
from fastapi import APIRouter, HTTPException
from app.schemas.anomaly import AnalyzeAnomalyRequest, AnomalyResponse
from app.services.db import (
    get_activity,
    get_user_activities,
    insert_anomaly,
    get_anomalies as db_get_anomalies,
)
from app.services.anomaly import vectorize_behavior, compute_anomaly_score
from app.services.gpt import generate_report

router = APIRouter()

@router.get("/get_anomalies", summary="Retrieve all stored anomaly reports")
async def get_anomalies():
    records = await db_get_anomalies()
    # convert ObjectId to string
    for r in records:
        r["_id"] = str(r["_id"])
    return records

@router.post(
    "/analyze_anomaly",
    response_model=AnomalyResponse,
    summary="Compute anomaly score and generate GPT report"
)
async def analyze_anomaly(req: AnalyzeAnomalyRequest):
    activity = await get_activity(req.activity_id)
    if not activity:
        raise HTTPException(404, "Activity not found")
    history = await get_user_activities(activity["user_id"], exclude_id=req.activity_id)
    if len(history) < 5:
        print(len(history))
        print(history)
        raise HTTPException(400, "Not enough historical data (need ≥5 records)")
    curr_vec = vectorize_behavior(activity)
    hist_mat = np.vstack([vectorize_behavior(h) for h in history])
    score, dev_feats = compute_anomaly_score(curr_vec, hist_mat)
    report = await generate_report(activity["user_id"], activity, score, dev_feats)

    anomaly_doc = {
        "user_id": activity["user_id"],
        "activity_id": req.activity_id,
        "anomaly_score": score,
        "deviant_features": dev_feats,
        "report": report
    }
    res = await insert_anomaly(anomaly_doc)

    return {
        "anomaly_id": str(res.inserted_id),
        **anomaly_doc
    }
