from pathlib import Path
import pandas as pd
import numpy as np
from ml.packaging.model_packaging import load_packaged_model

_MODEL_BUNDLE = None
_SEGMENT_CUSTOMERS_CACHE = None

def _get_bundle():
    global _MODEL_BUNDLE
    if _MODEL_BUNDLE is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        artifact_dir = project_root / "models" / "clustering" / "customer_kmeans_v1"
        _MODEL_BUNDLE = load_packaged_model(artifact_dir)
    return _MODEL_BUNDLE

def segment_customer(data):
    bundle = _get_bundle()
    model = bundle["model"]
    meta = bundle["metadata"]
    expected_features = meta.get("feature_order", [])

    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise TypeError("Input data must be a dict or a pandas DataFrame")

    missing = [col for col in expected_features if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    X = df[expected_features].astype(float)
    cluster_ids = model.predict(X)

    if isinstance(data, dict):
        return {
            "model_name": meta.get("model_name", "customer_kmeans_v1"),
            "model_version": meta.get("model_version", "v1"),
            "cluster_id": int(cluster_ids[0])
        }

    return {
        "model_name": meta.get("model_name", "customer_kmeans_v1"),
        "model_version": meta.get("model_version", "v1"),
        "cluster_id": [int(c) for c in cluster_ids]
    }

def get_customers_by_segment(cluster_id, limit=10):
    global _SEGMENT_CUSTOMERS_CACHE
    if _SEGMENT_CUSTOMERS_CACHE is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        ready_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_ready" / "track3_customer_clustering_ready.csv"
        customers_path = project_root / "real_estate_intelligence_dataset" / "processed" / "customers.csv"
        
        ready_df = pd.read_csv(ready_path)
        customers_df = pd.read_csv(customers_path)
        
        bundle = _get_bundle()
        model = bundle["model"]
        expected_features = bundle["metadata"]["feature_order"]
        
        X = ready_df[expected_features].astype(float)
        ready_df["cluster_id"] = model.predict(X)
        
        merged = ready_df[["customer_id", "cluster_id"]].merge(customers_df, on="customer_id")
        
        fields = [
            "customer_id", "customer_type", "customer_tier",
            "budget_min_egp", "budget_max_egp", "monthly_income_egp",
            "interaction_frequency", "preferred_location", "preferred_property_type"
        ]
        
        _SEGMENT_CUSTOMERS_CACHE = {}
        for c in range(4):
            sub = merged[merged["cluster_id"] == c][fields]
            _SEGMENT_CUSTOMERS_CACHE[c] = sub.to_dict(orient="records")
            
    records = _SEGMENT_CUSTOMERS_CACHE.get(cluster_id, [])
    return records[:limit]
