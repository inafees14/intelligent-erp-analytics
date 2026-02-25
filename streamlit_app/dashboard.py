"""Streamlit Analytics Dashboard.

Admin and Student analytics with statistical, ML, and Bayesian insights.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data_science.data_loader import get_analysis_dataframe
from data_science.statistical_analysis import (
    pearson_correlation, spearman_correlation, hypothesis_test_study_hours,
    linear_regression, anova_test, confidence_intervals, compute_vif,
)
from data_science.ml_models import regression_analysis, classification_analysis, clustering_analysis
from data_science.academic_intelligence import (
    train_prediction_model, train_risk_model, get_feature_importance,
)

st.set_page_config(page_title="Academic Intelligence Dashboard", layout="wide")

st.title("📊 Statistical & Bayesian Academic Intelligence Dashboard")

# Load data
@st.cache_data
def load_data():
    return get_analysis_dataframe()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", [
    "Overview",
    "Statistical Analysis",
    "Machine Learning",
    "Bayesian Analysis",
    "Student Insights",
])

# --- Overview ---
if page == "Overview":
    st.header("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df))
    col2.metric("Avg Total Marks", round(df["total_marks"].mean(), 2))
    col3.metric("Avg Study Hours", round(df["study_hours"].mean(), 2))
    col4.metric("Avg Attendance (absences)", round(df["attendance"].mean(), 2))

    st.subheader("Performance Distribution")
    st.bar_chart(df["total_marks"].value_counts().sort_index())

    st.subheader("Risk Distribution")
    fail_count = (df["total_marks"] < 10).sum()
    pass_count = (df["total_marks"] >= 10).sum()
    risk_df = pd.DataFrame({"Status": ["Pass", "Fail"], "Count": [pass_count, fail_count]})
    st.bar_chart(risk_df.set_index("Status"))

    st.subheader("Data Sample")
    st.dataframe(df.head(20))

# --- Statistical Analysis ---
elif page == "Statistical Analysis":
    st.header("Statistical Analysis")

    st.subheader("Pearson Correlation")
    pearson = pearson_correlation(df)
    st.dataframe(pearson.style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1))

    st.subheader("Spearman Correlation")
    spearman = spearman_correlation(df)
    st.dataframe(spearman.style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1))

    st.subheader("Hypothesis Test")
    ht = hypothesis_test_study_hours(df)
    st.json(ht)

    st.subheader("Linear Regression")
    lr = linear_regression(df)
    col1, col2 = st.columns(2)
    col1.metric("R²", lr["r_squared"])
    col2.metric("Adj R²", lr["adj_r_squared"])
    st.write("**Coefficients:**", lr["coefficients"])
    st.write("**P-values:**", lr["p_values"])

    st.subheader("ANOVA Test")
    anova = anova_test(df)
    st.json(anova)

    st.subheader("Confidence Intervals (Total Marks)")
    ci = confidence_intervals(df)
    st.json(ci)

    st.subheader("VIF (Multicollinearity)")
    vif = compute_vif(df)
    st.table(pd.DataFrame(vif))

# --- Machine Learning ---
elif page == "Machine Learning":
    st.header("Machine Learning Models")

    st.subheader("Regression Analysis")
    reg = regression_analysis(df)
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Linear Regression**")
        st.metric("RMSE", reg["linear_regression"]["rmse"])
        st.metric("MAE", reg["linear_regression"]["mae"])
        st.metric("R²", reg["linear_regression"]["r2"])
    with col2:
        st.write("**Random Forest**")
        st.metric("RMSE", reg["random_forest"]["rmse"])
        st.metric("MAE", reg["random_forest"]["mae"])
        st.metric("R²", reg["random_forest"]["r2"])

    st.subheader("Feature Importance (Regression)")
    imp = reg["random_forest"]["feature_importance"]
    st.bar_chart(pd.Series(imp))

    st.subheader("Classification Analysis")
    clf = classification_analysis(df)
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Logistic Regression**")
        st.metric("Accuracy", clf["logistic_regression"]["accuracy"])
        st.metric("F1 Score", clf["logistic_regression"]["f1_score"])
        if clf["logistic_regression"]["roc_auc"]:
            st.metric("ROC-AUC", clf["logistic_regression"]["roc_auc"])
        st.write("Confusion Matrix:", clf["logistic_regression"]["confusion_matrix"])
    with col2:
        st.write("**Random Forest Classifier**")
        st.metric("Accuracy", clf["random_forest"]["accuracy"])
        st.metric("F1 Score", clf["random_forest"]["f1_score"])
        if clf["random_forest"]["roc_auc"]:
            st.metric("ROC-AUC", clf["random_forest"]["roc_auc"])
        st.write("Confusion Matrix:", clf["random_forest"]["confusion_matrix"])

    st.subheader("Feature Importance (Classification)")
    clf_imp = clf["random_forest"]["feature_importance"]
    st.bar_chart(pd.Series(clf_imp))

    st.subheader("Clustering Analysis")
    clust = clustering_analysis(df)
    st.metric("Silhouette Score", clust["silhouette_score"])
    st.table(pd.DataFrame(clust["cluster_summary"]))

# --- Bayesian Analysis ---
elif page == "Bayesian Analysis":
    st.header("Bayesian Modelling (PyMC)")
    st.write("""
    **Model:**
    - Marks_i ~ Normal(μ_i, σ)
    - μ_i = α + β₁ × attendance + β₂ × study_hours

    **Priors:**
    - α ~ Normal(0, 10)
    - β ~ Normal(0, 10)
    - σ ~ HalfNormal(10)
    """)

    if st.button("Run Bayesian Model (may take a few minutes)"):
        with st.spinner("Sampling posterior..."):
            try:
                from data_science.bayesian_model import build_bayesian_model
                results = build_bayesian_model(df)
                if "error" in results:
                    st.error(results["error"])
                else:
                    st.subheader("Posterior Means")
                    st.json(results["posterior_means"])
                    st.subheader("Credible Intervals (94% HDI)")
                    st.json(results["credible_intervals"])
                    st.subheader("Interpretation")
                    for param, desc in results["interpretation"].items():
                        st.write(f"**{param}:** {desc}")
            except Exception as e:
                st.error(f"Bayesian model error: {e}")
    else:
        st.info("Click the button above to run the Bayesian model. This may take a few minutes.")

# --- Student Insights ---
elif page == "Student Insights":
    st.header("Individual Student Insights")

    pred_model, pred_features = train_prediction_model(df)
    risk_model, risk_features = train_risk_model(df)

    st.subheader("Enter Student Data")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.number_input("Subject 1 Marks", 0.0, 20.0, 10.0, 0.5)
        s2 = st.number_input("Subject 2 Marks", 0.0, 20.0, 10.0, 0.5)
        attendance = st.number_input("Absences", 0.0, 100.0, 5.0, 1.0)
    with col2:
        study_hours = st.number_input("Study Hours", 1.0, 4.0, 2.0, 0.5)
        failures = st.number_input("Past Failures", 0, 4, 0, 1)

    student_data = {
        "subject_1_marks": s1,
        "subject_2_marks": s2,
        "attendance": attendance,
        "study_hours": study_hours,
        "failures": failures,
    }

    if st.button("Generate Insights"):
        from data_science.academic_intelligence import predict_performance, compute_risk_probability, generate_student_insights
        predicted = predict_performance(pred_model, pred_features, student_data)
        risk = compute_risk_probability(risk_model, risk_features, student_data)
        insights = generate_student_insights(student_data, predicted, risk)

        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Marks", predicted)
        col2.metric("Risk Probability", f"{risk * 100:.1f}%")
        col3.metric("Risk Level", insights["risk_level"])

        st.subheader("Recommendations")
        for rec in insights["recommendations"]:
            st.write(f"- {rec}")

    st.subheader("Model Feature Importance")
    imp = get_feature_importance(pred_model, pred_features)
    st.bar_chart(pd.Series(imp))
