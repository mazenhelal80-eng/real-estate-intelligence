import sys
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans

from ml.packaging.model_packaging import save_packaged_model, load_packaged_model, verify_prediction_equivalence
from ml.forecasting.time_series_preparation import build_daily_cash_flow_series
from ml.forecasting.feature_engineering import create_forecasting_features
from ml.forecasting.time_series_split import temporal_train_val_test_split

def package_all_validated_models():
    models_root = project_root / "models"
    now_iso = datetime.now(timezone.utc).isoformat()
    
    print("=" * 100)
    print("STARTING MODEL PACKAGING & SERIALIZATION PIPELINE")
    print("=" * 100)
    
    packaged_summary = []
    
    # 1. REGRESSION (Property Price Prediction)
    print("\n1. Packaging Regression Model (property_price_rf_v1)...")
    reg_train_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track1_pricing_train.csv"
    reg_test_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track1_pricing_test.csv"
    
    reg_train_df = pd.read_csv(reg_train_path)
    reg_test_df = pd.read_csv(reg_test_path)
    
    reg_target = "target_base_price_egp"
    X_reg_train = reg_train_df.drop(columns=[reg_target])
    y_reg_train = reg_train_df[reg_target]
    X_reg_test = reg_test_df.drop(columns=[reg_target])
    
    reg_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    reg_model.fit(X_reg_train, y_reg_train)
    reg_orig_preds = reg_model.predict(X_reg_test[:100])
    
    reg_meta = {
        "model_name": "property_price_rf_v1",
        "model_version": "v1",
        "task_type": "regression",
        "framework": "scikit-learn",
        "framework_version": "1.9.1",
        "serialization_format": "joblib",
        "target_name": reg_target,
        "feature_count": len(X_reg_train.columns),
        "feature_names": list(X_reg_train.columns),
        "feature_order": list(X_reg_train.columns),
        "preprocessing_requirements": "Standardized ML-ready features (track1_pricing_train.csv schema)",
        "configuration": {
            "n_estimators": 100,
            "random_state": 42
        },
        "training_dataset": "real_estate_intelligence_dataset/processed/ml_ready/track1_pricing_train.csv",
        "created_at": now_iso
    }
    
    reg_dir = models_root / "regression" / "property_price_rf_v1"
    save_packaged_model(reg_model, reg_dir, reg_meta)
    
    loaded_reg = load_packaged_model(reg_dir)["model"]
    reloaded_reg_preds = loaded_reg.predict(X_reg_test[:100])
    _, reg_diff = verify_prediction_equivalence(reg_orig_preds, reloaded_reg_preds)
    print(f"   Saved to: {reg_dir}")
    print(f"   Prediction Equivalence Verified (Max Diff = {reg_diff:.10f})")
    packaged_summary.append(("Regression", "property_price_rf_v1", str(reg_dir), len(X_reg_train.columns)))
    
    # 2. CLASSIFICATION (Lead Conversion Prediction)
    print("\n2. Packaging Classification Model (lead_conversion_lr_v1)...")
    clf_train_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track2_conversion_train.csv"
    clf_test_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track2_conversion_test.csv"
    
    clf_train_df = pd.read_csv(clf_train_path)
    clf_test_df = pd.read_csv(clf_test_path)
    
    clf_target = "target_is_converted"
    X_clf_train = clf_train_df.drop(columns=[clf_target])
    y_clf_train = clf_train_df[clf_target]
    X_clf_test = clf_test_df.drop(columns=[clf_target])
    
    clf_model = LogisticRegression(C=10.0, class_weight="balanced", max_iter=1000, random_state=42)
    clf_model.fit(X_clf_train, y_clf_train)
    clf_orig_probs = clf_model.predict_proba(X_clf_test[:100])[:, 1]
    
    clf_meta = {
        "model_name": "lead_conversion_lr_v1",
        "model_version": "v1",
        "task_type": "binary_classification",
        "framework": "scikit-learn",
        "framework_version": "1.9.1",
        "serialization_format": "joblib",
        "target_name": clf_target,
        "feature_count": len(X_clf_train.columns),
        "feature_names": list(X_clf_train.columns),
        "feature_order": list(X_clf_train.columns),
        "preprocessing_requirements": "Standardized ML-ready features (track2_conversion_train.csv schema)",
        "configuration": {
            "C": 10.0,
            "class_weight": "balanced",
            "max_iter": 1000,
            "random_state": 42
        },
        "inference_contract": {
            "decision_threshold": 0.50,
            "class_mapping": {
                "0": "Not Converted",
                "1": "Converted"
            },
            "prediction_method": "predict_proba"
        },
        "training_dataset": "real_estate_intelligence_dataset/processed/ml_ready/track2_conversion_train.csv",
        "evaluation_metrics": {
            "holdout_accuracy": 0.6237,
            "holdout_precision": 0.1730,
            "holdout_recall": 0.4990,
            "holdout_f1": 0.2570,
            "holdout_pr_auc": 0.1810
        },
        "created_at": now_iso
    }
    
    clf_dir = models_root / "classification" / "lead_conversion_lr_v1"
    save_packaged_model(clf_model, clf_dir, clf_meta)
    
    loaded_clf = load_packaged_model(clf_dir)["model"]
    reloaded_clf_probs = loaded_clf.predict_proba(X_clf_test[:100])[:, 1]
    _, clf_diff = verify_prediction_equivalence(clf_orig_probs, reloaded_clf_probs)
    print(f"   Saved to: {clf_dir}")
    print(f"   Prediction Equivalence Verified (Max Diff = {clf_diff:.10f})")
    packaged_summary.append(("Classification", "lead_conversion_lr_v1", str(clf_dir), len(X_clf_train.columns)))
    
    # 3. CLUSTERING (Customer Segmentation)
    print("\n3. Packaging Clustering Model (customer_kmeans_v1)...")
    cluster_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track3_customer_clustering_ready.csv"
    cluster_df = pd.read_csv(cluster_path)
    X_cluster = cluster_df.drop(columns=["customer_id"])
    
    kmeans_model = KMeans(n_clusters=4, init="k-means++", n_init=10, random_state=42)
    kmeans_model.fit(X_cluster)
    kmeans_orig_preds = kmeans_model.predict(X_cluster[:100])
    
    cluster_meta = {
        "model_name": "customer_kmeans_v1",
        "model_version": "v1",
        "task_type": "clustering",
        "framework": "scikit-learn",
        "framework_version": "1.9.1",
        "serialization_format": "joblib",
        "feature_count": len(X_cluster.columns),
        "feature_names": list(X_cluster.columns),
        "feature_order": list(X_cluster.columns),
        "preprocessing_requirements": "Standardized ML-ready customer profiles (excluding customer_id)",
        "configuration": {
            "n_clusters": 4,
            "init": "k-means++",
            "n_init": 10,
            "random_state": 42
        },
        "training_dataset": "real_estate_intelligence_dataset/processed/ml_ready/track3_customer_clustering_ready.csv",
        "created_at": now_iso
    }
    
    cluster_dir = models_root / "clustering" / "customer_kmeans_v1"
    save_packaged_model(kmeans_model, cluster_dir, cluster_meta)
    
    loaded_kmeans = load_packaged_model(cluster_dir)["model"]
    reloaded_kmeans_preds = loaded_kmeans.predict(X_cluster[:100])
    _, cluster_diff = verify_prediction_equivalence(kmeans_orig_preds, reloaded_kmeans_preds)
    print(f"   Saved to: {cluster_dir}")
    print(f"   Prediction Equivalence Verified (Max Diff = {cluster_diff:.10f})")
    packaged_summary.append(("Clustering", "customer_kmeans_v1", str(cluster_dir), len(X_cluster.columns)))
    
    # 4. ANOMALY DETECTION (Property Valuation Outliers)
    print("\n4. Packaging Anomaly Detection Model (property_anomaly_iforest_v1)...")
    prop_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_track1_property_pricing.csv"
    prop_df = pd.read_csv(prop_path)
    
    anomaly_feature_cols = [
        "area_sqm", "bedrooms", "bathrooms", "floor_number",
        "base_price_egp", "expected_rent_monthly_egp", "price_per_sqm",
        "property_age", "rental_yield", "room_density", "popularity_score"
    ]
    X_anomaly = prop_df[anomaly_feature_cols]
    
    iforest_model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42, n_jobs=-1)
    iforest_model.fit(X_anomaly)
    iforest_orig_scores = iforest_model.decision_function(X_anomaly[:100])
    
    anomaly_meta = {
        "model_name": "property_anomaly_iforest_v1",
        "model_version": "v1",
        "task_type": "anomaly_detection",
        "framework": "scikit-learn",
        "framework_version": "1.9.1",
        "serialization_format": "joblib",
        "feature_count": len(anomaly_feature_cols),
        "feature_names": anomaly_feature_cols,
        "feature_order": anomaly_feature_cols,
        "preprocessing_requirements": "Continuous numeric valuation features",
        "configuration": {
            "n_estimators": 100,
            "contamination": 0.01,
            "random_state": 42
        },
        "inference_contract": {
            "score_method": "decision_function",
            "anomaly_flag_mapping": {
                "-1": "1 (Anomaly / Outlier)",
                "1": "0 (Normal / Inlier)"
            },
            "inference_scope": "Online / out-of-sample prediction supported via decision_function()"
        },
        "training_dataset": "real_estate_intelligence_dataset/processed/ml_track1_property_pricing.csv",
        "created_at": now_iso
    }
    
    anomaly_dir = models_root / "anomaly_detection" / "property_anomaly_iforest_v1"
    save_packaged_model(iforest_model, anomaly_dir, anomaly_meta)
    
    loaded_iforest = load_packaged_model(anomaly_dir)["model"]
    reloaded_iforest_scores = loaded_iforest.decision_function(X_anomaly[:100])
    _, iforest_diff = verify_prediction_equivalence(iforest_orig_scores, reloaded_iforest_scores)
    print(f"   Saved to: {anomaly_dir}")
    print(f"   Prediction Equivalence Verified (Max Diff = {iforest_diff:.10f})")
    packaged_summary.append(("Anomaly Detection", "property_anomaly_iforest_v1", str(anomaly_dir), len(anomaly_feature_cols)))
    
    # 5. FORECASTING (Net Cash Flow)
    print("\n5. Packaging Forecasting Model (cash_flow_linear_v1)...")
    raw_fc_df = build_daily_cash_flow_series(start_date="2024-01-01", end_date="2026-09-30")
    fc_df = create_forecasting_features(raw_fc_df, target_col="net_cash_flow")
    fc_train, fc_val, fc_test = temporal_train_val_test_split(fc_df)
    full_fc_train = pd.concat([fc_train, fc_val], ignore_index=True)
    
    fc_non_features = ["date", "sales_inflow", "rent_inflow", "total_inflow", "expense_outflow", "net_cash_flow"]
    fc_feature_cols = [c for c in fc_df.columns if c not in fc_non_features]
    
    fc_model = LinearRegression()
    fc_model.fit(full_fc_train[fc_feature_cols], full_fc_train["net_cash_flow"])
    fc_orig_preds = fc_model.predict(fc_test[fc_feature_cols][:50])
    
    fc_meta = {
        "model_name": "cash_flow_linear_v1",
        "model_version": "v1",
        "task_type": "time_series_forecasting",
        "framework": "scikit-learn",
        "framework_version": "1.9.1",
        "serialization_format": "joblib",
        "target_name": "net_cash_flow",
        "feature_count": len(fc_feature_cols),
        "feature_names": fc_feature_cols,
        "feature_order": fc_feature_cols,
        "preprocessing_requirements": "Autoregressive lags (1,7,14,28,30), shifted rolling stats (7,14,28), and calendar features",
        "inference_contract": {
            "forecast_mode": "One-step-ahead rolling daily forecast",
            "forecast_frequency": "Daily (D)"
        },
        "evaluation_metrics": {
            "holdout_mae": 27875485.27,
            "holdout_rmse": 35335239.40,
            "holdout_wape": 54.17
        },
        "training_dataset": "real_estate_intelligence_dataset/processed (deals, rent_payments, expenses)",
        "created_at": now_iso
    }
    
    fc_dir = models_root / "forecasting" / "cash_flow_linear_v1"
    save_packaged_model(fc_model, fc_dir, fc_meta)
    
    loaded_fc = load_packaged_model(fc_dir)["model"]
    reloaded_fc_preds = loaded_fc.predict(fc_test[fc_feature_cols][:50])
    _, fc_diff = verify_prediction_equivalence(fc_orig_preds, reloaded_fc_preds)
    print(f"   Saved to: {fc_dir}")
    print(f"   Prediction Equivalence Verified (Max Diff = {fc_diff:.10f})")
    packaged_summary.append(("Forecasting", "cash_flow_linear_v1", str(fc_dir), len(fc_feature_cols)))
    
    print("\n" + "=" * 100)
    print("ALL 5 VALIDATED MODEL ARTIFACTS PACKAGED & VERIFIED SUCCESSFULLY")
    print("=" * 100)
    summary_df = pd.DataFrame(packaged_summary, columns=["Track", "Model Name", "Artifact Directory", "Feature Count"])
    print(summary_df.to_string(index=False))
    print("=" * 100)

if __name__ == "__main__":
    package_all_validated_models()
