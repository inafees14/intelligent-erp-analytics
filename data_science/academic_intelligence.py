"""Academic Intelligence Layer.

Predict student future performance, compute risk probability,
generate feature importance, and provide student insights.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler


def train_prediction_model(df: pd.DataFrame):
    """Train a Random Forest model for predicting total_marks."""
    features = ["subject_1_marks", "subject_2_marks", "attendance", "study_hours"]
    X = df[features].values
    y = df["total_marks"].values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, features


def train_risk_model(df: pd.DataFrame, threshold: float = 10.0):
    """Train a classifier for risk prediction (fail probability)."""
    features = ["subject_1_marks", "subject_2_marks", "attendance", "study_hours", "failures"]
    X = df[features].values
    y = (df["total_marks"] < threshold).astype(int).values

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, features


def predict_performance(model, features: list, student_data: dict) -> float:
    """Predict a student's future performance."""
    X = np.array([[student_data.get(f, 0) for f in features]])
    return round(float(model.predict(X)[0]), 2)


def compute_risk_probability(model, features: list, student_data: dict) -> float:
    """Compute the probability of a student being at risk of failure."""
    X = np.array([[student_data.get(f, 0) for f in features]])
    proba = model.predict_proba(X)
    if proba.shape[1] > 1:
        return round(float(proba[0][1]), 4)
    return 0.0


def get_feature_importance(model, feature_names: list) -> dict:
    """Get feature importance from a trained model."""
    return {f: round(float(i), 4) for f, i in zip(feature_names, model.feature_importances_)}


def generate_student_insights(
    student_data: dict,
    predicted_marks: float,
    risk_prob: float,
) -> dict:
    """Generate insights for a student."""
    insights = {
        "predicted_performance": predicted_marks,
        "risk_probability": risk_prob,
        "risk_level": "High" if risk_prob > 0.5 else ("Medium" if risk_prob > 0.2 else "Low"),
        "recommendations": [],
    }

    if student_data.get("study_hours", 0) < 2:
        insights["recommendations"].append("Increase study hours to at least 2 hours daily.")
    if student_data.get("attendance", 0) > 10:
        insights["recommendations"].append("High absences detected. Improve attendance.")
    if student_data.get("failures", 0) > 0:
        insights["recommendations"].append("Past failures noted. Consider additional tutoring.")
    if risk_prob > 0.5:
        insights["recommendations"].append("⚠️ High risk of underperformance. Immediate intervention recommended.")

    if not insights["recommendations"]:
        insights["recommendations"].append("Performance is on track. Keep up the good work!")

    return insights
