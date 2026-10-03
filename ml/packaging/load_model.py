from pathlib import Path
import pandas as pd
import numpy as np
from ml.packaging.model_packaging import load_packaged_model

def get_loaded_model_bundle(model_dir):
    bundle = load_packaged_model(model_dir)
    model = bundle["model"]
    meta = bundle["metadata"]
    
    feature_order = meta.get("feature_order", [])
    task_type = meta.get("task_type", "")
    contract = meta.get("inference_contract", {})
    threshold = contract.get("decision_threshold", 0.5)
    
    def predict(input_data):
        if isinstance(input_data, pd.DataFrame):
            assert list(input_data.columns) == feature_order, "Input columns do not match feature contract!"
            X = input_data[feature_order]
        else:
            arr = np.array(input_data)
            assert arr.shape[1] == len(feature_order), "Feature count mismatch!"
            X = pd.DataFrame(arr, columns=feature_order)
            
        if task_type == "binary_classification":
            probs = model.predict_proba(X)[:, 1]
            binary_preds = (probs >= threshold).astype(int)
            return {
                "predictions": binary_preds,
                "probabilities": probs,
                "threshold": threshold
            }
        elif task_type == "anomaly_detection":
            raw_preds = model.predict(X)
            scores = model.decision_function(X) if hasattr(model, "decision_function") else None
            anomaly_flags = (raw_preds == -1).astype(int)
            return {
                "anomalies": anomaly_flags,
                "scores": scores
            }
        else:
            return {"predictions": model.predict(X)}
            
    return {
        "model": model,
        "metadata": meta,
        "feature_order": feature_order,
        "predict_fn": predict
    }
