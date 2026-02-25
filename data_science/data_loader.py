"""Load and transform UCI Student Performance Dataset into ERP-compatible format."""

import os
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATASET_PATH = os.path.join(DATA_DIR, "student-mat.csv")


def load_raw_dataset() -> pd.DataFrame:
    """Load the raw UCI student-mat.csv dataset."""
    return pd.read_csv(DATASET_PATH, sep=";")


def transform_to_erp(df: pd.DataFrame) -> pd.DataFrame:
    """Map UCI dataset columns to ERP-compatible schema.

    Mapping:
        G1 -> subject_1_marks
        G2 -> subject_2_marks
        G3 -> total_marks
        absences -> attendance
        studytime -> study_hours
        failures -> failures (risk indicator)
    """
    erp_df = pd.DataFrame()
    erp_df["subject_1_marks"] = df["G1"].astype(float)
    erp_df["subject_2_marks"] = df["G2"].astype(float)
    erp_df["total_marks"] = df["G3"].astype(float)
    erp_df["attendance"] = df["absences"].astype(float)
    erp_df["study_hours"] = df["studytime"].astype(float)
    erp_df["failures"] = df["failures"].astype(int)
    return erp_df


def get_analysis_dataframe() -> pd.DataFrame:
    """Return the transformed ERP-compatible DataFrame for analysis."""
    raw = load_raw_dataset()
    return transform_to_erp(raw)
