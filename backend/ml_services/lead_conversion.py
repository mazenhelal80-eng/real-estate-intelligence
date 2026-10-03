from pathlib import Path
import pandas as pd
import numpy as np
from ml.packaging.model_packaging import load_packaged_model

_MODEL_BUNDLE = None

def _get_bundle():
    global _MODEL_BUNDLE
    if _MODEL_BUNDLE is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        artifact_dir = project_root / "models" / "classification" / "lead_conversion_lr_v1"
        _MODEL_BUNDLE = load_packaged_model(artifact_dir)
    return _MODEL_BUNDLE

def predict_lead_conversion(data):
    bundle = _get_bundle()
    model = bundle["model"]
    meta = bundle["metadata"]
    expected_features = meta.get("feature_order", [])
    contract = meta.get("inference_contract", {})
    threshold = float(contract.get("decision_threshold", 0.50))
    class_mapping = contract.get("class_mapping", {"0": "Not Converted", "1": "Converted"})

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
    probabilities = model.predict_proba(X)[:, 1]
    binary_predictions = (probabilities >= threshold).astype(int)

    if isinstance(data, dict):
        pred_int = int(binary_predictions[0])
        return {
            "model_name": meta.get("model_name", "lead_conversion_lr_v1"),
            "model_version": meta.get("model_version", "v1"),
            "probability": float(probabilities[0]),
            "threshold": threshold,
            "prediction": pred_int,
            "class_label": class_mapping.get(str(pred_int), "Converted" if pred_int == 1 else "Not Converted")
        }

    return {
        "model_name": meta.get("model_name", "lead_conversion_lr_v1"),
        "model_version": meta.get("model_version", "v1"),
        "probability": [float(p) for p in probabilities],
        "threshold": threshold,
        "prediction": [int(p) for p in binary_predictions],
        "class_label": [class_mapping.get(str(p), "Converted" if p == 1 else "Not Converted") for p in binary_predictions]
    }
