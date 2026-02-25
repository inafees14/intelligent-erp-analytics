"""Machine Learning Module.

Provides regression (Linear, Random Forest), classification
(Logistic Regression, Random Forest), and clustering (KMeans).
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    roc_auc_score, f1_score, confusion_matrix, accuracy_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


# ---------- Regression ----------

def regression_analysis(df: pd.DataFrame) -> dict:
    """Compare Linear Regression vs Random Forest Regression for predicting total_marks."""
    features = ["subject_1_marks", "subject_2_marks", "attendance", "study_hours"]
    X = df[features].values
    y = df["total_marks"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    results = {
        "linear_regression": {
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, lr_pred))), 4),
            "mae": round(float(mean_absolute_error(y_test, lr_pred)), 4),
            "r2": round(float(r2_score(y_test, lr_pred)), 4),
            "coefficients": {f: round(float(c), 4) for f, c in zip(features, lr.coef_)},
        },
        "random_forest": {
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, rf_pred))), 4),
            "mae": round(float(mean_absolute_error(y_test, rf_pred)), 4),
            "r2": round(float(r2_score(y_test, rf_pred)), 4),
            "feature_importance": {f: round(float(i), 4) for f, i in zip(features, rf.feature_importances_)},
        },
        "feature_names": features,
    }
    return results


# ---------- Classification ----------

def classification_analysis(df: pd.DataFrame, fail_threshold: float = 10.0) -> dict:
    """Classify students as fail/pass. Fail=1 if total_marks < threshold."""
    features = ["subject_1_marks", "subject_2_marks", "attendance", "study_hours", "failures"]
    X = df[features].values
    y = (df["total_marks"] < fail_threshold).astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Logistic Regression
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train, y_train)
    log_pred = log_reg.predict(X_test)
    log_prob = log_reg.predict_proba(X_test)[:, 1] if len(np.unique(y_train)) > 1 else np.zeros(len(X_test))

    # Random Forest Classifier
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_train, y_train)
    rf_pred = rf_clf.predict(X_test)
    rf_prob = rf_clf.predict_proba(X_test)[:, 1] if len(np.unique(y_train)) > 1 else np.zeros(len(X_test))

    results = {
        "fail_threshold": fail_threshold,
        "logistic_regression": {
            "accuracy": round(float(accuracy_score(y_test, log_pred)), 4),
            "f1_score": round(float(f1_score(y_test, log_pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, log_prob)), 4) if len(np.unique(y_test)) > 1 else None,
            "confusion_matrix": confusion_matrix(y_test, log_pred).tolist(),
        },
        "random_forest": {
            "accuracy": round(float(accuracy_score(y_test, rf_pred)), 4),
            "f1_score": round(float(f1_score(y_test, rf_pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, rf_prob)), 4) if len(np.unique(y_test)) > 1 else None,
            "confusion_matrix": confusion_matrix(y_test, rf_pred).tolist(),
            "feature_importance": {f: round(float(i), 4) for f, i in zip(features, rf_clf.feature_importances_)},
        },
        "feature_names": features,
    }
    return results


# ---------- Clustering ----------

def clustering_analysis(df: pd.DataFrame, n_clusters: int = 3) -> dict:
    """KMeans clustering for student performance grouping."""
    features = ["subject_1_marks", "subject_2_marks", "total_marks", "attendance", "study_hours"]
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, labels)

    cluster_summary = []
    for c in range(n_clusters):
        mask = labels == c
        cluster_df = df[features].iloc[mask]
        cluster_summary.append({
            "cluster": c,
            "size": int(mask.sum()),
            "mean_total_marks": round(float(cluster_df["total_marks"].mean()), 2),
            "mean_attendance": round(float(cluster_df["attendance"].mean()), 2),
            "mean_study_hours": round(float(cluster_df["study_hours"].mean()), 2),
        })

    return {
        "n_clusters": n_clusters,
        "silhouette_score": round(float(sil_score), 4),
        "cluster_summary": cluster_summary,
        "labels": labels.tolist(),
        "feature_names": features,
    }


def run_all_ml(df: pd.DataFrame) -> dict:
    """Run all ML analyses."""
    return {
        "regression": regression_analysis(df),
        "classification": classification_analysis(df),
        "clustering": clustering_analysis(df),
    }
