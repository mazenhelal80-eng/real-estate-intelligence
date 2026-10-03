from pathlib import Path
import pandas as pd
import numpy as np
from ml.packaging.model_packaging import load_packaged_model

_MODEL_BUNDLE = None

def _get_bundle():
    global _MODEL_BUNDLE
    if _MODEL_BUNDLE is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        artifact_dir = project_root / "models" / "anomaly_detection" / "property_anomaly_iforest_v1"
        _MODEL_BUNDLE = load_packaged_model(artifact_dir)
    return _MODEL_BUNDLE

def detect_property_anomaly(data):
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
    scores = model.decision_function(X)
    flags = (scores < 0).astype(int)

    if isinstance(data, dict):
        return {
            "model_name": meta.get("model_name", "property_anomaly_iforest_v1"),
            "model_version": meta.get("model_version", "v1"),
            "anomaly_flag": int(flags[0]),
            "anomaly_score": float(scores[0])
        }

    return {
        "model_name": meta.get("model_name", "property_anomaly_iforest_v1"),
        "model_version": meta.get("model_version", "v1"),
        "anomaly_flag": [int(f) for f in flags],
        "anomaly_score": [float(s) for s in scores]
    }
