"""Tests for data science modules."""

import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def sample_df():
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "subject_1_marks": np.random.randint(0, 21, n).astype(float),
        "subject_2_marks": np.random.randint(0, 21, n).astype(float),
        "total_marks": np.random.randint(0, 21, n).astype(float),
        "attendance": np.random.randint(0, 50, n).astype(float),
        "study_hours": np.random.choice([1, 2, 3, 4], n).astype(float),
        "failures": np.random.choice([0, 1, 2, 3], n, p=[0.7, 0.15, 0.1, 0.05]),
    })


def test_data_loader():
    from data_science.data_loader import load_raw_dataset, transform_to_erp, get_analysis_dataframe
    raw = load_raw_dataset()
    assert "G1" in raw.columns
    assert "G2" in raw.columns
    assert "G3" in raw.columns
    assert len(raw) > 0

    erp = transform_to_erp(raw)
    assert "subject_1_marks" in erp.columns
    assert "total_marks" in erp.columns
    assert "attendance" in erp.columns

    df = get_analysis_dataframe()
    assert len(df) > 0


def test_pearson_correlation(sample_df):
    from data_science.statistical_analysis import pearson_correlation
    corr = pearson_correlation(sample_df)
    assert corr.shape[0] == 5
    assert corr.shape[1] == 5
    # Diagonal should be 1
    for col in corr.columns:
        assert abs(corr.loc[col, col] - 1.0) < 0.001


def test_spearman_correlation(sample_df):
    from data_science.statistical_analysis import spearman_correlation
    corr = spearman_correlation(sample_df)
    assert corr.shape == (5, 5)


def test_hypothesis_test(sample_df):
    from data_science.statistical_analysis import hypothesis_test_study_hours
    result = hypothesis_test_study_hours(sample_df)
    assert "t_statistic" in result
    assert "p_value" in result
    assert "significant" in result


def test_linear_regression_stats(sample_df):
    from data_science.statistical_analysis import linear_regression
    result = linear_regression(sample_df)
    assert "r_squared" in result
    assert "coefficients" in result
    assert "p_values" in result


def test_anova(sample_df):
    from data_science.statistical_analysis import anova_test
    result = anova_test(sample_df)
    assert "f_statistic" in result
    assert "p_value" in result


def test_confidence_intervals(sample_df):
    from data_science.statistical_analysis import confidence_intervals
    result = confidence_intervals(sample_df)
    assert result["ci_lower"] < result["ci_upper"]
    assert result["confidence_level"] == 0.95


def test_vif(sample_df):
    from data_science.statistical_analysis import compute_vif
    result = compute_vif(sample_df)
    assert len(result) == 3  # const + 2 features


def test_regression_analysis(sample_df):
    from data_science.ml_models import regression_analysis
    result = regression_analysis(sample_df)
    assert "linear_regression" in result
    assert "random_forest" in result
    assert "rmse" in result["linear_regression"]
    assert "feature_importance" in result["random_forest"]


def test_classification_analysis(sample_df):
    from data_science.ml_models import classification_analysis
    result = classification_analysis(sample_df)
    assert "logistic_regression" in result
    assert "random_forest" in result
    assert "accuracy" in result["logistic_regression"]
    assert "confusion_matrix" in result["random_forest"]


def test_clustering_analysis(sample_df):
    from data_science.ml_models import clustering_analysis
    result = clustering_analysis(sample_df)
    assert result["n_clusters"] == 3
    assert "silhouette_score" in result
    assert len(result["cluster_summary"]) == 3


def test_academic_intelligence(sample_df):
    from data_science.academic_intelligence import (
        train_prediction_model, train_risk_model,
        predict_performance, compute_risk_probability,
        get_feature_importance, generate_student_insights,
    )
    pred_model, pred_features = train_prediction_model(sample_df)
    risk_model, risk_features = train_risk_model(sample_df)

    student = {
        "subject_1_marks": 12.0,
        "subject_2_marks": 10.0,
        "attendance": 5.0,
        "study_hours": 3.0,
        "failures": 0,
    }

    predicted = predict_performance(pred_model, pred_features, student)
    assert isinstance(predicted, float)

    risk = compute_risk_probability(risk_model, risk_features, student)
    assert 0 <= risk <= 1

    importance = get_feature_importance(pred_model, pred_features)
    assert len(importance) > 0

    insights = generate_student_insights(student, predicted, risk)
    assert "predicted_performance" in insights
    assert "risk_level" in insights
    assert "recommendations" in insights
