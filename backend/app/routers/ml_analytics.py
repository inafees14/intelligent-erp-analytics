import os
import pickle
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Student, Marks  # Ensure Marks is imported

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning Analytics"]
)

# Load the Model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "saved_models", "model_xgb_final.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        xgb_model = pickle.load(f)
except Exception as e:
    xgb_model = None

@router.get("/status")
def model_status():
    # We check if the xgb_model successfully loaded into memory at startup
    if xgb_model is not None:
        return {"model_status": "trained"}
    else:
        return {"model_status": "not trained"}

@router.get("/predict-risk/{student_id}")
def predict_student_risk(student_id: int, db: Session = Depends(get_db)):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="ML Model is not available.")
        
    # 1. Fetch Student's Marks/Engagement data
    # We fetch all marks for this student to calculate averages/sums
    student_marks = db.query(Marks).filter(Marks.student_id == student_id).all()
    
    if not student_marks:
        raise HTTPException(status_code=404, detail="No academic records found for this student")

    # 2. Aggregate the data (Just like Cell 7 & 11 in your train.ipynb)
    total_clicks = sum(mark.engagement_clicks for mark in student_marks if mark.engagement_clicks)
    avg_prev_attempts = max(mark.num_of_prev_attempts for mark in student_marks if mark.num_of_prev_attempts) or 0
    
    # Calculate average score from sessional and endsem
    total_score = sum((mark.sessional_marks or 0) + (mark.endsem_marks or 0) for mark in student_marks)
    avg_score = total_score / len(student_marks) if student_marks else 0

    # Assuming standard credits and weights if not in DB (Update if you have these in DB!)
    studied_credits = 60 * len(student_marks) 
    total_weight = 100 * len(student_marks)

    # 3. Calculate the engineered features from your notebook
    engagement_per_credit = total_clicks / (studied_credits + 1)
    performance_index = (avg_score * total_weight) / 100

    # 4. Construct the exact DataFrame the model expects
    feature_dict = {
        "num_of_prev_attempts": [avg_prev_attempts],
        "studied_credits": [studied_credits],
        "score": [avg_score],
        "weight": [total_weight],
        "sum_click": [total_clicks],
        "engagement_per_credit": [engagement_per_credit],
        "performance_index": [performance_index]
    }
    
    df_features = pd.DataFrame(feature_dict)
    
    # 5. Make Prediction
    risk_probability = xgb_model.predict_proba(df_features)[0][1] 
    prediction_class = int(xgb_model.predict(df_features)[0])
    
    return {
        "student_id": student_id,
        "prediction": "At Risk" if prediction_class == 0 else "On Track", # Adjust 0/1 based on your target mapping
        "risk_probability": round(float(risk_probability), 3),
        "model_inputs": feature_dict 
    }