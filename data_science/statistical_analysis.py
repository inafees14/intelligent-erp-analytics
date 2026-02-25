"""Statistical Analysis Module.

Provides correlation, hypothesis testing, regression, ANOVA,
residual diagnostics, confidence intervals, and VIF analysis.
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm


def pearson_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Pearson correlation matrix."""
    cols = ["subject_1_marks", "subject_2_marks", "total_marks", "attendance", "study_hours"]
    return df[cols].corr(method="pearson")


def spearman_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Spearman correlation matrix."""
    cols = ["subject_1_marks", "subject_2_marks", "total_marks", "attendance", "study_hours"]
    return df[cols].corr(method="spearman")


def hypothesis_test_study_hours(df: pd.DataFrame) -> dict:
    """Test whether study_hours significantly affects total_marks.

    Uses independent t-test: high study hours (>=3) vs low (<3).
    """
    high = df[df["study_hours"] >= 3]["total_marks"]
    low = df[df["study_hours"] < 3]["total_marks"]
    t_stat, p_value = stats.ttest_ind(high, low, equal_var=False)
    return {
        "test": "Independent t-test (study_hours effect on total_marks)",
        "t_statistic": round(float(t_stat), 4),
        "p_value": round(float(p_value), 6),
        "significant": p_value < 0.05,
        "high_mean": round(float(high.mean()), 2),
        "low_mean": round(float(low.mean()), 2),
    }


def linear_regression(df: pd.DataFrame) -> dict:
    """OLS linear regression: total_marks ~ attendance + study_hours."""
    X = df[["attendance", "study_hours"]].copy()
    X = sm.add_constant(X)
    y = df["total_marks"]
    model = sm.OLS(y, X).fit()
    return {
        "r_squared": round(model.rsquared, 4),
        "adj_r_squared": round(model.rsquared_adj, 4),
        "f_statistic": round(float(model.fvalue), 4),
        "f_pvalue": round(float(model.f_pvalue), 6),
        "coefficients": {k: round(float(v), 4) for k, v in model.params.items()},
        "p_values": {k: round(float(v), 6) for k, v in model.pvalues.items()},
        "residuals": model.resid.tolist(),
        "fitted_values": model.fittedvalues.tolist(),
    }


def anova_test(df: pd.DataFrame) -> dict:
    """One-way ANOVA: total_marks across study_hours groups."""
    groups = [group["total_marks"].values for _, group in df.groupby("study_hours")]
    f_stat, p_value = stats.f_oneway(*groups)
    return {
        "test": "One-way ANOVA (total_marks by study_hours groups)",
        "f_statistic": round(float(f_stat), 4),
        "p_value": round(float(p_value), 6),
        "significant": p_value < 0.05,
    }


def confidence_intervals(df: pd.DataFrame, column: str = "total_marks", confidence: float = 0.95) -> dict:
    """Compute confidence interval for a column."""
    data = df[column].dropna()
    mean = data.mean()
    se = stats.sem(data)
    ci = stats.t.interval(confidence, len(data) - 1, loc=mean, scale=se)
    return {
        "column": column,
        "mean": round(float(mean), 4),
        "std_error": round(float(se), 4),
        "confidence_level": confidence,
        "ci_lower": round(float(ci[0]), 4),
        "ci_upper": round(float(ci[1]), 4),
    }


def compute_vif(df: pd.DataFrame) -> list:
    """Compute Variance Inflation Factor for multicollinearity check."""
    features = df[["attendance", "study_hours"]].dropna()
    features = sm.add_constant(features)
    vif_data = []
    for i, col in enumerate(features.columns):
        vif_data.append({
            "feature": col,
            "vif": round(float(variance_inflation_factor(features.values, i)), 4),
        })
    return vif_data


def run_all_analyses(df: pd.DataFrame) -> dict:
    """Run all statistical analyses and return results."""
    return {
        "pearson_correlation": pearson_correlation(df).to_dict(),
        "spearman_correlation": spearman_correlation(df).to_dict(),
        "hypothesis_test": hypothesis_test_study_hours(df),
        "linear_regression": linear_regression(df),
        "anova": anova_test(df),
        "confidence_intervals": confidence_intervals(df),
        "vif": compute_vif(df),
    }
