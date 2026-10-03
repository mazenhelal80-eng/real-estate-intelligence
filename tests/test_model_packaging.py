import unittest
import json
from pathlib import Path
import numpy as np
import pandas as pd

from ml.packaging.model_packaging import load_packaged_model
from ml.packaging.load_model import get_loaded_model_bundle

class TestModelPackaging(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.models_root = self.project_root / "models"
        self.expected_models = [
            ("regression", "property_price_rf_v1", 37),
            ("classification", "lead_conversion_lr_v1", 27),
            ("clustering", "customer_kmeans_v1", 16),
            ("anomaly_detection", "property_anomaly_iforest_v1", 11),
            ("forecasting", "cash_flow_linear_v1", 17)
        ]

    def test_01_artifact_and_metadata_files_exist(self):
        for track, model_name, _ in self.expected_models:
            model_dir = self.models_root / track / model_name
            self.assertTrue(model_dir.exists(), f"Directory missing: {model_dir}")
            
            model_file = model_dir / "model.joblib"
            metadata_file = model_dir / "metadata.json"
            
            self.assertTrue(model_file.exists(), f"model.joblib missing in {model_dir}")
            self.assertTrue(metadata_file.exists(), f"metadata.json missing in {model_dir}")
            self.assertGreater(model_file.stat().st_size, 0, f"Empty model file in {model_dir}")
            self.assertGreater(metadata_file.stat().st_size, 0, f"Empty metadata file in {model_dir}")

    def test_02_metadata_schema_and_feature_contract(self):
        required_keys = [
            "model_name", "model_version", "task_type", "framework",
            "serialization_format", "feature_count", "feature_names", "feature_order"
        ]
        
        for track, model_name, expected_feature_count in self.expected_models:
            model_dir = self.models_root / track / model_name
            metadata_file = model_dir / "metadata.json"
            
            with open(metadata_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
            for k in required_keys:
                self.assertIn(k, meta, f"Key '{k}' missing from {metadata_file}")
                
            self.assertEqual(meta["model_version"], "v1")
            self.assertEqual(meta["serialization_format"], "joblib")
            self.assertEqual(meta["feature_count"], expected_feature_count)
            self.assertEqual(len(meta["feature_names"]), expected_feature_count)
            self.assertEqual(len(meta["feature_order"]), expected_feature_count)
            self.assertEqual(meta["feature_names"], meta["feature_order"])
            
            if "target_name" in meta and meta["target_name"]:
                self.assertNotIn(meta["target_name"], meta["feature_names"], "Target leaked into feature names!")

    def test_03_classification_threshold_contract(self):
        clf_meta_file = self.models_root / "classification" / "lead_conversion_lr_v1" / "metadata.json"
        with open(clf_meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        contract = meta.get("inference_contract", {})
        self.assertIn("decision_threshold", contract)
        self.assertEqual(contract["decision_threshold"], 0.50)
        self.assertIn("class_mapping", contract)

    def test_04_model_deserialization_and_inference(self):
        for track, model_name, feature_count in self.expected_models:
            model_dir = self.models_root / track / model_name
            bundle = get_loaded_model_bundle(model_dir)
            
            self.assertIsNotNone(bundle["model"])
            self.assertEqual(len(bundle["feature_order"]), feature_count)
            
            dummy_sample = pd.DataFrame(
                np.zeros((3, feature_count)),
                columns=bundle["feature_order"]
            )
            
            result = bundle["predict_fn"](dummy_sample)
            self.assertIsInstance(result, dict)
            
            if "predictions" in result:
                self.assertEqual(len(result["predictions"]), 3)
            elif "anomalies" in result:
                self.assertEqual(len(result["anomalies"]), 3)

if __name__ == "__main__":
    unittest.main()
