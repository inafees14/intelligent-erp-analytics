"""Bayesian Modelling Module using PyMC.

Model:
    Marks_i ~ Normal(mu_i, sigma)
    mu_i = alpha + beta1 * attendance + beta2 * study_hours

Priors:
    alpha ~ Normal(0, 10)
    beta ~ Normal(0, 10)
    sigma ~ HalfNormal(10)
"""

import numpy as np
import pandas as pd

try:
    import pymc as pm
    import arviz as az
    PYMC_AVAILABLE = True
except ImportError:
    PYMC_AVAILABLE = False


def build_bayesian_model(df: pd.DataFrame) -> dict:
    """Build and sample from the Bayesian model.

    Returns posterior summary, credible intervals, and diagnostics.
    """
    if not PYMC_AVAILABLE:
        return {"error": "PyMC is not installed. Install with: pip install pymc arviz"}

    attendance = df["attendance"].values.astype(float)
    study_hours = df["study_hours"].values.astype(float)
    total_marks = df["total_marks"].values.astype(float)

    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sigma=10)
        beta1 = pm.Normal("beta1", mu=0, sigma=10)
        beta2 = pm.Normal("beta2", mu=0, sigma=10)
        sigma = pm.HalfNormal("sigma", sigma=10)

        mu = alpha + beta1 * attendance + beta2 * study_hours
        likelihood = pm.Normal("marks", mu=mu, sigma=sigma, observed=total_marks)

        trace = pm.sample(1000, tune=500, cores=1, return_inferencedata=True, random_seed=42)
        ppc = pm.sample_posterior_predictive(trace, random_seed=42)

    summary = az.summary(trace, var_names=["alpha", "beta1", "beta2", "sigma"])

    results = {
        "summary": summary.to_dict(),
        "posterior_means": {
            "alpha": round(float(summary.loc["alpha", "mean"]), 4),
            "beta1": round(float(summary.loc["beta1", "mean"]), 4),
            "beta2": round(float(summary.loc["beta2", "mean"]), 4),
            "sigma": round(float(summary.loc["sigma", "mean"]), 4),
        },
        "credible_intervals": {
            "alpha": {
                "lower": round(float(summary.loc["alpha", "hdi_3%"]), 4),
                "upper": round(float(summary.loc["alpha", "hdi_97%"]), 4),
            },
            "beta1": {
                "lower": round(float(summary.loc["beta1", "hdi_3%"]), 4),
                "upper": round(float(summary.loc["beta1", "hdi_97%"]), 4),
            },
            "beta2": {
                "lower": round(float(summary.loc["beta2", "hdi_3%"]), 4),
                "upper": round(float(summary.loc["beta2", "hdi_97%"]), 4),
            },
            "sigma": {
                "lower": round(float(summary.loc["sigma", "hdi_3%"]), 4),
                "upper": round(float(summary.loc["sigma", "hdi_97%"]), 4),
            },
        },
        "interpretation": {
            "alpha": "Baseline expected marks when attendance=0 and study_hours=0",
            "beta1": "Change in expected marks per unit increase in attendance (absences)",
            "beta2": "Change in expected marks per unit increase in study hours",
            "sigma": "Residual standard deviation (uncertainty in predictions)",
        },
    }
    return results
