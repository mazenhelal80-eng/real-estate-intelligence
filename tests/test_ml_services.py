import unittest
import pandas as pd
import numpy as np
from pathlib import Path

from backend.ml_services.price_prediction import predict_property_price, _get_bundle as get_price_bundle
from backend.ml_services.lead_conversion import predict_lead_conversion, _get_bundle as get_lead_bundle
from backend.ml_services.customer_segmentation import segment_customer, _get_bundle as get_cust_bundle
from backend.ml_services.property_anomaly import detect_property_anomaly, _get_bundle as get_anom_bundle
from backend.ml_services.cash_flow_forecast import forecast_cash_flow, _get_bundle as get_fc_bundle

class TestMLServices(unittest.TestCase):
    def test_01_price_prediction_service(self):
        bundle = get_price_bundle()
        features = bundle["metadata"]["feature_order"]
        sample_input = {feat: 1.0 for feat in features}
        
        result = predict_property_price(sample_input)
        self.assertEqual(result["model_name"], "property_price_rf_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertEqual(result["target_name"], "target_base_price_egp")
        self.assertIsInstance(result["predicted_price_egp"], float)

        df_input = pd.DataFrame([sample_input, sample_input])
        batch_result = predict_property_price(df_input)
        self.assertEqual(len(batch_result["predicted_price_egp"]), 2)

    def test_02_lead_conversion_service_threshold_and_labels(self):
        bundle = get_lead_bundle()
        features = bundle["metadata"]["feature_order"]
        sample_input = {feat: 0.5 for feat in features}

        result = predict_lead_conversion(sample_input)
        self.assertEqual(result["model_name"], "lead_conversion_lr_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertEqual(result["threshold"], 0.50)
        self.assertIn(result["prediction"], [0, 1])
        self.assertIn(result["class_label"], ["Converted", "Not Converted"])
        self.assertIsInstance(result["probability"], float)

        df_input = pd.DataFrame([sample_input, sample_input])
        batch_result = predict_lead_conversion(df_input)
        self.assertEqual(len(batch_result["prediction"]), 2)
        self.assertEqual(len(batch_result["class_label"]), 2)

    def test_03_customer_segmentation_service(self):
        bundle = get_cust_bundle()
        features = bundle["metadata"]["feature_order"]
        sample_input = {feat: 0.0 for feat in features}

        result = segment_customer(sample_input)
        self.assertEqual(result["model_name"], "customer_kmeans_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertIsInstance(result["cluster_id"], int)
        self.assertIn(result["cluster_id"], [0, 1, 2, 3])

        df_input = pd.DataFrame([sample_input, sample_input])
        batch_result = segment_customer(df_input)
        self.assertEqual(len(batch_result["cluster_id"]), 2)

    def test_04_property_anomaly_service(self):
        bundle = get_anom_bundle()
        features = bundle["metadata"]["feature_order"]
        sample_input = {feat: 100.0 for feat in features}

        result = detect_property_anomaly(sample_input)
        self.assertEqual(result["model_name"], "property_anomaly_iforest_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertIn(result["anomaly_flag"], [0, 1])
        self.assertIsInstance(result["anomaly_score"], float)
        if result["anomaly_score"] < 0:
            self.assertEqual(result["anomaly_flag"], 1)
        else:
            self.assertEqual(result["anomaly_flag"], 0)

    def test_05_cash_flow_forecast_service_direct_features(self):
        bundle = get_fc_bundle()
        features = bundle["metadata"]["feature_order"]
        sample_input = {feat: 100000.0 for feat in features}

        result = forecast_cash_flow(sample_input, forecast_date="2026-10-01")
        self.assertEqual(result["model_name"], "cash_flow_linear_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertEqual(result["forecast_date"], "2026-10-01")
        self.assertIsInstance(result["predicted_net_cash_flow"], float)

    def test_06_cash_flow_forecast_service_historical_series(self):
        dates = pd.date_range("2026-01-01", periods=45, freq="D")
        np.random.seed(42)
        values = np.random.normal(500000, 50000, size=len(dates))
        df_history = pd.DataFrame({"date": dates, "net_cash_flow": values})

        result = forecast_cash_flow(df_history, forecast_date="2026-02-15")
        self.assertEqual(result["model_name"], "cash_flow_linear_v1")
        self.assertEqual(result["model_version"], "v1")
        self.assertEqual(result["forecast_date"], "2026-02-15")
        self.assertIsInstance(result["predicted_net_cash_flow"], float)

    def test_07_validation_missing_features(self):
        invalid_input = {"area_sqm": 120}
        with self.assertRaises(ValueError):
            predict_property_price(invalid_input)
        with self.assertRaises(ValueError):
            predict_lead_conversion(invalid_input)
        with self.assertRaises(ValueError):
            segment_customer(invalid_input)
        with self.assertRaises(ValueError):
            detect_property_anomaly(invalid_input)

    def test_08_insufficient_time_series_history(self):
        short_dates = pd.date_range("2026-01-01", periods=10, freq="D")
        short_df = pd.DataFrame({"date": short_dates, "net_cash_flow": np.ones(10)})
        with self.assertRaises(ValueError):
            forecast_cash_flow(short_df)

    def test_09_model_bundle_caching(self):
        b1 = get_price_bundle()
        b2 = get_price_bundle()
        self.assertIs(b1, b2)

if __name__ == "__main__":
    unittest.main()
