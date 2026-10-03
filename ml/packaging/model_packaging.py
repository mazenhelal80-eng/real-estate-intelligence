import json
from pathlib import Path
import joblib
import numpy as np

def save_packaged_model(model_obj, target_dir, metadata_dict):
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    model_file = target_path / "model.joblib"
    metadata_file = target_path / "metadata.json"
    
    joblib.dump(model_obj, model_file)
    
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata_dict, f, indent=2, ensure_ascii=False)
        
    return model_file, metadata_file

def load_packaged_model(target_dir):
    target_path = Path(target_dir)
    model_file = target_path / "model.joblib"
    metadata_file = target_path / "metadata.json"
    
    assert model_file.exists(), f"Model artifact missing at {model_file}"
    assert metadata_file.exists(), f"Metadata missing at {metadata_file}"
    
    model_obj = joblib.load(model_file)
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata_dict = json.load(f)
        
    return {
        "model": model_obj,
        "metadata": metadata_dict,
        "model_file": model_file,
        "metadata_file": metadata_file
    }

def verify_prediction_equivalence(original_preds, reloaded_preds, tolerance=1e-7):
    orig = np.array(original_preds)
    reloaded = np.array(reloaded_preds)
    assert orig.shape == reloaded.shape, f"Shape mismatch: {orig.shape} vs {reloaded.shape}"
    max_diff = np.max(np.abs(orig - reloaded))
    assert max_diff <= tolerance, f"Prediction mismatch exceeding tolerance: {max_diff}"
    return True, float(max_diff)
