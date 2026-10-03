"""
Phase 3 - Section 3.3: ML Pipeline & Leakage-Safe Data Splitting Engine
Purpose: Partition datasets into train/test splits (temporal & stratified), fit preprocessors
         strictly on training data, and export final modeling tensors/CSVs.
Output:
  - real_estate_intelligence_dataset/processed/ml_ready/*.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder


def build_ml_ready_datasets() -> None:
    project_root = Path(__file__).resolve().parent.parent
    processed_dir = project_root / "real_estate_intelligence_dataset" / "processed"
    ml_ready_dir = processed_dir / "ml_ready"
    ml_ready_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("PHASE 3.3: LEAKAGE-SAFE ML PIPELINE & SPLITTING")
    print("=" * 80)

    # -------------------------------------------------------------
    # 1. TRACK 1: PROPERTY PRICE PREDICTION PIPELINE
    # -------------------------------------------------------------
    t1_raw = pd.read_csv(processed_dir / "ml_track1_property_pricing.csv")
    
    # Target
    y_t1 = t1_raw["base_price_egp"]
    
    # Leakage-Guarded Predictor Features
    # Explicitly drop base_price_egp, price_per_sqm, rental_yield, annual_expected_rent, and raw IDs
    t1_drop_cols = [
        "base_price_egp", "price_per_sqm", "rental_yield", "annual_expected_rent",
        "expected_rent_monthly_egp", "unit_id", "project_id", "construction_year",
        "is_area_iqr_outlier", "is_outlier"
    ]
    X_t1 = t1_raw.drop(columns=[col for col in t1_drop_cols if col in t1_raw.columns])

    # Stratified 80/20 Train-Test Split by property_type
    X_t1_train, X_t1_test, y_t1_train, y_t1_test = train_test_split(
        X_t1, y_t1, test_size=0.20, random_state=42, stratify=X_t1["property_type"]
    )

    # Define ColumnTransformer
    t1_num_cols = ["area_sqm", "bedrooms", "bathrooms", "floor_number", "property_age", "room_density", "popularity_score"]
    t1_cat_cols = ["property_type", "finishing_type", "location", "developer_name", "construction_status"]

    t1_preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), t1_num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), t1_cat_cols)
        ]
    )

    # Fit strictly on X_train
    X_t1_train_trans = t1_preprocessor.fit_transform(X_t1_train)
    X_t1_test_trans = t1_preprocessor.transform(X_t1_test)

    # Get feature names
    cat_names = t1_preprocessor.named_transformers_["cat"].get_feature_names_out(t1_cat_cols)
    all_t1_features = t1_num_cols + list(cat_names)

    # Save ready CSVs
    df_t1_train = pd.DataFrame(X_t1_train_trans, columns=all_t1_features)
    df_t1_train["target_base_price_egp"] = y_t1_train.values
    df_t1_train.to_csv(ml_ready_dir / "track1_pricing_train.csv", index=False, encoding="utf-8")

    df_t1_test = pd.DataFrame(X_t1_test_trans, columns=all_t1_features)
    df_t1_test["target_base_price_egp"] = y_t1_test.values
    df_t1_test.to_csv(ml_ready_dir / "track1_pricing_test.csv", index=False, encoding="utf-8")

    print(f"-> Track 1 (Property Pricing): Train {df_t1_train.shape} | Test {df_t1_test.shape} (Stratified 80/20)")

    # -------------------------------------------------------------
    # 2. TRACK 2: LEAD CONVERSION PREDICTION PIPELINE
    # -------------------------------------------------------------
    t2_raw = pd.read_csv(processed_dir / "ml_track2_lead_conversion.csv")
    
    # Sort chronologically by lead_date
    t2_raw["lead_date"] = pd.to_datetime(t2_raw["lead_date"])
    t2_sorted = t2_raw.sort_values("lead_date").reset_index(drop=True)

    y_t2 = t2_sorted["is_converted"]
    
    # Leakage-Guarded Predictors (Drop IDs, Dates, and Target)
    t2_drop_cols = ["lead_id", "customer_id", "listing_id", "unit_id", "agent_id", "is_converted", "lead_date", "lead_status"]
    X_t2 = t2_sorted.drop(columns=[col for col in t2_drop_cols if col in t2_sorted.columns])

    # Chronological 80/20 Split
    split_idx = int(len(X_t2) * 0.80)
    X_t2_train, X_t2_test = X_t2.iloc[:split_idx], X_t2.iloc[split_idx:]
    y_t2_train, y_t2_test = y_t2.iloc[:split_idx], y_t2.iloc[split_idx:]

    t2_num_cols = [
        "lead_score", "interaction_count", "monthly_income_egp", "budget_max_egp",
        "budget_spread_egp", "income_to_budget_ratio", "listing_price_egp"
    ]
    t2_cat_cols = ["lead_source", "customer_type", "customer_tier", "interaction_frequency", "listing_type"]

    t2_preprocessor = ColumnTransformer(
        transformers=[
            ("num", RobustScaler(), t2_num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), t2_cat_cols)
        ]
    )

    # Fit strictly on X_train
    X_t2_train_trans = t2_preprocessor.fit_transform(X_t2_train)
    X_t2_test_trans = t2_preprocessor.transform(X_t2_test)

    cat_t2_names = t2_preprocessor.named_transformers_["cat"].get_feature_names_out(t2_cat_cols)
    all_t2_features = t2_num_cols + list(cat_t2_names)

    df_t2_train = pd.DataFrame(X_t2_train_trans, columns=all_t2_features)
    df_t2_train["target_is_converted"] = y_t2_train.values
    df_t2_train.to_csv(ml_ready_dir / "track2_conversion_train.csv", index=False, encoding="utf-8")

    df_t2_test = pd.DataFrame(X_t2_test_trans, columns=all_t2_features)
    df_t2_test["target_is_converted"] = y_t2_test.values
    df_t2_test.to_csv(ml_ready_dir / "track2_conversion_test.csv", index=False, encoding="utf-8")

    print(f"-> Track 2 (Lead Conversion): Train {df_t2_train.shape} | Test {df_t2_test.shape} (Chronological 80/20)")

    # -------------------------------------------------------------
    # 3. TRACK 3: CUSTOMER SEGMENTATION CLUSTERING MATRIX
    # -------------------------------------------------------------
    t3_raw = pd.read_csv(processed_dir / "ml_track3_customer_segmentation.csv")
    t3_num_cols = ["budget_min_egp", "budget_max_egp", "budget_spread_egp", "monthly_income_egp", "income_to_budget_ratio"]
    t3_cat_cols = ["customer_type", "customer_tier", "interaction_frequency"]

    t3_preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), t3_num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), t3_cat_cols)
        ]
    )
    X_t3_trans = t3_preprocessor.fit_transform(t3_raw[t3_num_cols + t3_cat_cols])
    cat_t3_names = t3_preprocessor.named_transformers_["cat"].get_feature_names_out(t3_cat_cols)
    all_t3_features = t3_num_cols + list(cat_t3_names)

    df_t3 = pd.DataFrame(X_t3_trans, columns=all_t3_features)
    df_t3.insert(0, "customer_id", t3_raw["customer_id"].values)
    df_t3.to_csv(ml_ready_dir / "track3_customer_clustering_ready.csv", index=False, encoding="utf-8")

    print(f"-> Track 3 (Customer Clustering): Full population matrix {df_t3.shape}")

    print("=" * 80)
    print(f"-> Successfully exported all ML-ready datasets to: {ml_ready_dir.relative_to(project_root)}")
    print("=" * 80)


if __name__ == "__main__":
    build_ml_ready_datasets()
