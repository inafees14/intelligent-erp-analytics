from fastapi import APIRouter
import os

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.get("/status")
def model_status():

    if os.path.exists("ml_models/student_model.pkl"):
        return {"model_status": "trained"}
    else:
        return {"model_status": "not trained"}

@router.get("/predict-risk/{student_id}")
def predict_risk(student_id: int):

    # placeholder until model is trained
    return {
        "student_id": student_id,
        "prediction": "Model not trained yet",
        "risk_level": "unknown"
    }