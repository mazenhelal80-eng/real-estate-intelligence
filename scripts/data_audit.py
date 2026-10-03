"""
Phase 3 - Section 3.1: Automated Raw Data Audit Engine
Purpose: Recursively inspect all raw CSV files, compute dataset & column metrics,
         and generate structured audit reports for Data Prep & Feature Engineering.
Outputs:
  - reports/data_audit.csv (Dataset-level summary)
  - reports/data_audit_column_details.csv (Column-level detailed stats)
"""

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd


def discover_raw_files(raw_dir: Path) -> List[Path]:
    """Discover all CSV files in the raw dataset directory in sorted order."""
    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")
    csv_files = sorted(list(raw_dir.glob("*.csv")))
    if not csv_files:
        raise ValueError(f"No CSV files found in {raw_dir}")
    return csv_files


def classify_column_type(series: pd.Series, col_name: str) -> str:
    """
    Classify column semantic role into: ID, Date, Boolean, Numeric, or Categorical.
    """
    col_lower = col_name.lower()
    dtype = series.dtype

    # ID detection
    if col_lower.endswith("_id") or col_lower == "id":
        return "ID"

    # Date detection heuristics
    if any(date_kw in col_lower for date_kw in ["date", "time", "due", "launch", "hired", "created"]):
        return "Date"

    # Boolean detection
    if pd.api.types.is_bool_dtype(dtype):
        return "Boolean"
    if series.dropna().isin([0, 1, True, False, "True", "False"]).all() and series.nunique() <= 2:
        if "id" not in col_lower and "count" not in col_lower:
            return "Boolean"

    # Numeric detection
    if pd.api.types.is_numeric_dtype(dtype):
        return "Numeric"

    # Default to Categorical / String
    return "Categorical"


def audit_single_dataset(file_path: Path) -> Tuple[Dict, List[Dict]]:
    """
    Load and audit a single raw CSV dataset.
    Returns:
      - dataset_summary: Dict with table-level metadata.
      - column_details: List of Dicts with per-column statistics.
    """
    df = pd.read_csv(file_path)
    file_name = file_path.name
    total_rows, total_cols = df.shape
    total_cells = total_rows * total_cols

    # Missing values & duplicate rows
    null_counts_per_col = df.isna().sum()
    total_missing_cells = int(null_counts_per_col.sum())
    missing_pct = round((total_missing_cells / total_cells * 100) if total_cells > 0 else 0.0, 2)
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = round((duplicate_rows / total_rows * 100) if total_rows > 0 else 0.0, 2)

    cols_with_nulls = [col for col, count in null_counts_per_col.items() if count > 0]
    cols_with_nulls_str = ", ".join(cols_with_nulls) if cols_with_nulls else "None"

    # Column-level inspection
    column_details = []
    numeric_col_count = 0
    cat_col_count = 0
    date_col_count = 0
    id_col_count = 0
    bool_col_count = 0

    for col in df.columns:
        series = df[col]
        semantic_role = classify_column_type(series, col)

        if semantic_role == "Numeric":
            numeric_col_count += 1
        elif semantic_role == "Categorical":
            cat_col_count += 1
        elif semantic_role == "Date":
            date_col_count += 1
        elif semantic_role == "ID":
            id_col_count += 1
        elif semantic_role == "Boolean":
            bool_col_count += 1

        non_null_count = int(series.count())
        null_count = int(series.isna().sum())
        null_col_pct = round((null_count / total_rows * 100) if total_rows > 0 else 0.0, 2)
        unique_count = int(series.nunique(dropna=True))
        unique_ratio = round((unique_count / non_null_count) if non_null_count > 0 else 0.0, 4)

        # Descriptive statistics for numeric columns
        min_val, max_val, mean_val, std_val = None, None, None, None
        if pd.api.types.is_numeric_dtype(series.dtype):
            min_val = round(float(series.min()), 2) if non_null_count > 0 else None
            max_val = round(float(series.max()), 2) if non_null_count > 0 else None
            mean_val = round(float(series.mean()), 2) if non_null_count > 0 else None
            std_val = round(float(series.std()), 2) if non_null_count > 1 else None

        # Sample values representation
        sample_vals = series.dropna().unique()[:3].tolist()
        sample_vals_str = str(sample_vals)

        column_details.append({
            "file_name": file_name,
            "column_name": col,
            "semantic_role": semantic_role,
            "pandas_dtype": str(series.dtype),
            "total_rows": total_rows,
            "non_null_count": non_null_count,
            "null_count": null_count,
            "null_percentage": null_col_pct,
            "unique_count": unique_count,
            "unique_ratio": unique_ratio,
            "min_value": min_val,
            "max_value": max_val,
            "mean_value": mean_val,
            "std_value": std_val,
            "sample_values": sample_vals_str,
        })

    dataset_summary = {
        "file_name": file_name,
        "total_rows": total_rows,
        "total_columns": total_cols,
        "total_missing_cells": total_missing_cells,
        "missing_cells_percentage": missing_pct,
        "duplicate_rows_count": duplicate_rows,
        "duplicate_rows_percentage": duplicate_pct,
        "numeric_columns_count": numeric_col_count,
        "categorical_columns_count": cat_col_count,
        "date_columns_count": date_col_count,
        "id_columns_count": id_col_count,
        "boolean_columns_count": bool_col_count,
        "columns_with_missing_values": cols_with_nulls_str,
    }

    return dataset_summary, column_details


def run_data_audit() -> None:
    """Run full automated data audit across all raw CSVs and save reports."""
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("STARTING RAW DATASET AUDIT (PHASE 3 FOUNDATION)")
    print("=" * 80)

    csv_files = discover_raw_files(raw_dir)
    print(f"Discovered {len(csv_files)} raw CSV files in {raw_dir.relative_to(project_root)}:\n")

    all_summaries = []
    all_column_details = []

    for idx, file_path in enumerate(csv_files, 1):
        summary, col_details = audit_single_dataset(file_path)
        all_summaries.append(summary)
        all_column_details.extend(col_details)
        print(f"[{idx:02d}/13] Audited: {summary['file_name']:<20} | Rows: {summary['total_rows']:>6,d} | Cols: {summary['total_columns']:>2d} | Missing: {summary['total_missing_cells']:>4d} | Duplicates: {summary['duplicate_rows_count']}")

    # Create DataFrames
    summary_df = pd.DataFrame(all_summaries)
    col_details_df = pd.DataFrame(all_column_details)

    # Save CSV reports
    summary_out_path = reports_dir / "data_audit.csv"
    col_details_out_path = reports_dir / "data_audit_column_details.csv"

    summary_df.to_csv(summary_out_path, index=False, encoding="utf-8")
    col_details_df.to_csv(col_details_out_path, index=False, encoding="utf-8")

    print("=" * 80)
    print("AUDIT COMPLETE:")
    print(f"1. Dataset Summary Saved: {summary_out_path.relative_to(project_root)} ({len(summary_df)} datasets)")
    print(f"2. Column Details Saved:  {col_details_out_path.relative_to(project_root)} ({len(col_details_df)} total columns inspected)")
    print("=" * 80)


if __name__ == "__main__":
    run_data_audit()
