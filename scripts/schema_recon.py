"""
Phase 1 - Task 003-B: Schema & Data Quality Reconnaissance Script
Purpose: Inspect schemas, infer types, detect candidate primary/foreign keys,
         evaluate basic data quality, and export machine-readable reports.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np


def classify_column(col_name: str, series: pd.Series) -> str:
    """Classifies a column into numeric, boolean, datetime, categorical/object, or other."""
    # 1. Check boolean
    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    # 2. Check numeric (integer / float)
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    # 3. Check datetime dtype
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    col_lower = col_name.lower()
    is_date_name = any(keyword in col_lower for keyword in ["date", "time", "_at", "timestamp", "year"])

    is_string_like = (
        pd.api.types.is_string_dtype(series) or
        pd.api.types.is_object_dtype(series) or
        isinstance(series.dtype, pd.CategoricalDtype)
    )

    if is_string_like:
        if is_date_name:
            non_nulls = series.dropna()
            if len(non_nulls) > 0:
                sample = non_nulls.head(50)
                try:
                    pd.to_datetime(sample, errors="raise")
                    return "datetime"
                except (ValueError, TypeError):
                    pass
        return "categorical/object"

    return "other"


def run_schema_recon():
    project_root = Path(__file__).resolve().parent.parent
    raw_data_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("PHASE 1: SCHEMA & DATA QUALITY RECONNAISSANCE (TASK 003-B)")
    print(f"Scanning directory: {raw_data_dir}")
    print("=" * 70)

    if not raw_data_dir.exists():
        print(f"ERROR: Raw data directory not found: {raw_data_dir}", file=sys.stderr)
        return False

    csv_files = sorted(raw_data_dir.glob("*.csv"))
    if not csv_files:
        print(f"ERROR: No CSV files found in {raw_data_dir}", file=sys.stderr)
        return False

    # Load all tables into memory for structural and relationship analysis
    tables = {}
    for csv_file in csv_files:
        table_name = csv_file.stem
        try:
            df = pd.read_csv(csv_file)
            tables[table_name] = {"path": csv_file, "df": df}
        except Exception as e:
            print(f"ERROR: Failed to load {csv_file.name}: {e}", file=sys.stderr)
            return False

    print(f"Discovered and loaded {len(tables)} tables.\n")

    schema_rows = []
    quality_rows = []
    candidate_pks = {}

    # -------------------------------------------------------------
    # TASK 1, 2, 4: Table-Level Inspection & Data Quality
    # -------------------------------------------------------------
    for table_name, data in tables.items():
        df = data["df"]
        num_rows, num_cols = df.shape
        dup_rows = int(df.duplicated().sum())
        total_missing_cells = int(df.isnull().sum().sum())

        table_pks = []
        date_cols = []
        constant_cols = []
        cols_with_missing = []

        print("=" * 70)
        print(f"TABLE: {table_name}.csv")
        print("=" * 70)
        print(f"Rows:            {num_rows:,}")
        print(f"Columns:         {num_cols}")
        print(f"Duplicate rows:  {dup_rows:,}")
        print(f"Missing cells:   {total_missing_cells:,}")
        print("\n## COLUMNS")
        print(f"{'Column Name':<28} {'Dtype':<15} {'Inferred Type':<20} {'Missing':<10} {'Missing %':<12} {'Unique':<10}")
        print("-" * 98)

        for col in df.columns:
            series = df[col]
            dtype_str = str(series.dtype)
            inferred_type = classify_column(col, series)
            n_missing = int(series.isnull().sum())
            pct_missing = round((n_missing / num_rows) * 100, 2) if num_rows > 0 else 0.0
            n_unique = int(series.nunique(dropna=False))

            # Primary Key Candidate test: no nulls, all rows unique, non-empty table
            is_candidate_pk = bool(n_missing == 0 and series.is_unique and num_rows > 0)
            if is_candidate_pk and col.lower().endswith("id"):
                table_pks.append(col)

            if inferred_type == "datetime":
                date_cols.append(col)
            if n_unique <= 1:
                constant_cols.append(col)
            if n_missing > 0:
                cols_with_missing.append(col)

            schema_rows.append({
                "table_name": table_name,
                "column_name": col,
                "pandas_dtype": dtype_str,
                "inferred_type": inferred_type,
                "missing_count": n_missing,
                "missing_percentage": pct_missing,
                "unique_count": n_unique,
                "is_candidate_pk": is_candidate_pk
            })

            print(f"{col:<28} {dtype_str:<15} {inferred_type:<20} {n_missing:<10} {f'{pct_missing}%':<12} {n_unique:<10}")

        candidate_pks[table_name] = table_pks

        print("\n## CANDIDATE PRIMARY KEY(S)")
        if table_pks:
            for pk in table_pks:
                print(f"  * {pk}")
        else:
            print("  * None detected (no unique non-null ID column)")

        quality_rows.append({
            "table_name": table_name,
            "total_rows": num_rows,
            "total_columns": num_cols,
            "duplicate_rows": dup_rows,
            "missing_cells": total_missing_cells,
            "missing_columns_count": len(cols_with_missing),
            "missing_columns_list": ";".join(cols_with_missing) if cols_with_missing else "None",
            "constant_columns_count": len(constant_cols),
            "candidate_pk_columns": ";".join(table_pks) if table_pks else "None",
            "date_columns_count": len(date_cols),
            "date_columns_list": ";".join(date_cols) if date_cols else "None"
        })
        print()

    # -------------------------------------------------------------
    # TASK 3: Candidate Foreign Keys & Relationship Mapping
    # -------------------------------------------------------------
    print("=" * 70)
    print("## CANDIDATE RELATIONSHIP MAPPINGS (FOREIGN KEYS)")
    print("=" * 70)

    relationship_rows = []

    # Map candidate FK column patterns to likely referenced tables
    id_to_target_table = {
        "project_id": "projects",
        "unit_id": "units",
        "customer_id": "customers",
        "agent_id": "agents",
        "listing_id": "listings",
        "lead_id": "leads",
        "viewing_id": "viewings",
        "deal_id": "deals",
        "tenant_id": "tenants",
        "lease_id": "leases",
        "maintenance_id": "maintenance",
        "expense_id": "expenses",
        "payment_id": "rent_payments"
    }

    for source_tbl, data in tables.items():
        src_df = data["df"]

        for col in src_df.columns:
            # An ID column referencing another table is a candidate foreign key
            if col.endswith("_id") and col in id_to_target_table:
                target_tbl = id_to_target_table[col]
                if target_tbl == source_tbl:
                    continue

                if target_tbl in tables and col in tables[target_tbl]["df"].columns:
                    target_df = tables[target_tbl]["df"]
                    src_keys = src_df[col].dropna().unique()
                    tgt_keys = set(target_df[col].dropna().unique())

                    matched = [k for k in src_keys if k in tgt_keys]
                    unmatched = [k for k in src_keys if k not in tgt_keys]

                    match_pct = round((len(matched) / len(src_keys)) * 100, 2) if len(src_keys) > 0 else 100.0
                    match_status = "VALID" if len(unmatched) == 0 else "PARTIAL_MISMATCH"

                    relationship_rows.append({
                        "source_table": source_tbl,
                        "foreign_key_column": col,
                        "target_table": target_tbl,
                        "target_column": col,
                        "match_status": match_status,
                        "total_distinct_foreign_keys": len(src_keys),
                        "matched_keys_count": len(matched),
                        "unmatched_keys_count": len(unmatched),
                        "match_percentage": match_pct
                    })

                    print(f"{source_tbl}.{col} -> {target_tbl}.{col}")
                    print(f"  -> MATCH STATUS: {match_status} ({len(matched)}/{len(src_keys)} distinct keys matched, {match_pct}%)")

    # -------------------------------------------------------------
    # TASK 5: Export Machine-Readable Reports
    # -------------------------------------------------------------
    schema_df = pd.DataFrame(schema_rows)
    quality_df = pd.DataFrame(quality_rows)
    rel_df = pd.DataFrame(relationship_rows)

    schema_report_path = reports_dir / "schema_report.csv"
    quality_report_path = reports_dir / "data_quality_recon.csv"
    rel_report_path = reports_dir / "relationship_candidates.csv"

    schema_df.to_csv(schema_report_path, index=False, encoding="utf-8")
    quality_df.to_csv(quality_report_path, index=False, encoding="utf-8")
    rel_df.to_csv(rel_report_path, index=False, encoding="utf-8")

    print("\n" + "=" * 70)
    print("REPORTS GENERATED:")
    print(f"  * {schema_report_path.relative_to(project_root)}")
    print(f"  * {quality_report_path.relative_to(project_root)}")
    print(f"  * {rel_report_path.relative_to(project_root)}")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = run_schema_recon()
    sys.exit(0 if success else 1)
