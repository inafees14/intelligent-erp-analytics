import os
import pickle
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Student, Marks

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning Analytics"]
)

# Load the Model Safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "saved_models", "model_xgb_final.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        xgb_model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    xgb_model = None

@router.get("/status")
def model_status():
    if xgb_model is not None:
        return {"model_status": "trained"}
    return {"model_status": "not trained"}

# CHANGED: Accept a string (enroll_no) in the URL
@router.get("/predict-risk/{enroll_no}")
def predict_student_risk(enroll_no: str, db: Session = Depends(get_db)):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="ML Model is not available on the server.")
        
    # 1. Fetch Student by Enrollment Number
    student = db.query(Student).filter(Student.enrollment_number == enroll_no).first()
    
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with enrollment {enroll_no} not found")

    # 2. Fetch Student's Marks/Engagement data using their internal ID
    student_marks = db.query(Marks).filter(Marks.student_id == student.id).all()
    
    if not student_marks:
        raise HTTPException(status_code=404, detail="No academic records found for this student")

    # Aggregate the data safely
    total_clicks = sum((mark.engagement_clicks or 0) for mark in student_marks)
    
    attempts = [mark.num_of_prev_attempts for mark in student_marks if mark.num_of_prev_attempts is not None]
    avg_prev_attempts = max(attempts) if attempts else 0
    
    total_score = sum((mark.sessional_marks or 0) + (mark.endsem_marks or 0) for mark in student_marks)
    avg_score = total_score / len(student_marks) if student_marks else 0

    studied_credits = 60 * len(student_marks) 
    total_weight = 100 * len(student_marks)

    engagement_per_credit = total_clicks / (studied_credits + 1)
    performance_index = (avg_score * total_weight) / 100

    # Construct the exact DataFrame the model expects
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
    
    # Make Prediction
    try:
        risk_probability = xgb_model.predict_proba(df_features)[0][1] 
        prediction_class = int(xgb_model.predict(df_features)[0])
        
        return {
            "enrollment_number": enroll_no,
            "student_name": f"{student.first_name} {student.last_name}", # Bonus: Return their name for the UI!
            "prediction": "At Risk" if prediction_class == 0 else "On Track", 
            "risk_probability": round(float(risk_probability), 3),
            "model_inputs": feature_dict 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")