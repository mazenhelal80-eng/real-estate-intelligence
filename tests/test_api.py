import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import numpy as np
import pandas as pd

from backend.api.main import app
from backend.ml_services.price_prediction import _get_bundle as get_price_bundle
from backend.ml_services.lead_conversion import _get_bundle as get_lead_bundle
from backend.ml_services.customer_segmentation import _get_bundle as get_cust_bundle
from backend.ml_services.property_anomaly import _get_bundle as get_anom_bundle
from backend.ml_services.cash_flow_forecast import _get_bundle as get_fc_bundle

class TestFastAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["version"], "1.0.0")

    def test_02_openapi_json(self):
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("paths", data)
        self.assertIn("/api/v1/ml/price-prediction", data["paths"])
        self.assertIn("/api/v1/ml/lead-conversion", data["paths"])
        self.assertIn("/api/v1/ml/customer-segmentation", data["paths"])
        self.assertIn("/api/v1/ml/property-anomaly", data["paths"])
        self.assertIn("/api/v1/ml/cash-flow-forecast", data["paths"])

    def test_03_price_prediction_endpoint(self):
        features = get_price_bundle()["metadata"]["feature_order"]
        payload = {feat: 1.0 for feat in features}
        response = self.client.post("/api/v1/ml/price-prediction", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "property_price_rf_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertIn("predicted_price_egp", data)
        self.assertEqual(data["target_name"], "target_base_price_egp")
        self.assertIsInstance(data["predicted_price_egp"], float)

    def test_04_lead_conversion_endpoint(self):
        features = get_lead_bundle()["metadata"]["feature_order"]
        payload = {feat: 0.5 for feat in features}
        response = self.client.post("/api/v1/ml/lead-conversion", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "lead_conversion_lr_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertEqual(data["threshold"], 0.50)
        self.assertIn(data["prediction"], [0, 1])
        self.assertIn(data["class_label"], ["Converted", "Not Converted"])
        self.assertIsInstance(data["probability"], float)

    def test_05_customer_segmentation_endpoint(self):
        features = get_cust_bundle()["metadata"]["feature_order"]
        payload = {feat: 0.0 for feat in features}
        response = self.client.post("/api/v1/ml/customer-segmentation", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "customer_kmeans_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertIn(data["cluster_id"], [0, 1, 2, 3])

    def test_06_property_anomaly_endpoint(self):
        features = get_anom_bundle()["metadata"]["feature_order"]
        payload = {feat: 100.0 for feat in features}
        response = self.client.post("/api/v1/ml/property-anomaly", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "property_anomaly_iforest_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertIn(data["anomaly_flag"], [0, 1])
        self.assertIsInstance(data["anomaly_score"], float)

    def test_07_cash_flow_forecast_direct(self):
        features = get_fc_bundle()["metadata"]["feature_order"]
        payload = {feat: 100000.0 for feat in features}
        payload["forecast_date"] = "2026-10-01"
        response = self.client.post("/api/v1/ml/cash-flow-forecast", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "cash_flow_linear_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertEqual(data["forecast_date"], "2026-10-01")
        self.assertIsInstance(data["predicted_net_cash_flow"], float)

    def test_08_cash_flow_forecast_historical_series(self):
        dates = pd.date_range("2026-01-01", periods=45, freq="D")
        np.random.seed(42)
        values = np.random.normal(500000, 50000, size=len(dates))
        series = [{"date": d.strftime("%Y-%m-%d"), "net_cash_flow": float(v)} for d, v in zip(dates, values)]
        payload = {
            "forecast_date": "2026-02-15",
            "historical_series": series
        }
        response = self.client.post("/api/v1/ml/cash-flow-forecast", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "cash_flow_linear_v1")
        self.assertEqual(data["model_version"], "v1")
        self.assertEqual(data["forecast_date"], "2026-02-15")
        self.assertIsInstance(data["predicted_net_cash_flow"], float)

    def test_09_validation_error_handling_422(self):
        invalid_payload = {"area_sqm": 120}
        response = self.client.post("/api/v1/ml/price-prediction", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

        response = self.client.post("/api/v1/ml/lead-conversion", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

        response = self.client.post("/api/v1/ml/customer-segmentation", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

        response = self.client.post("/api/v1/ml/property-anomaly", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

    def test_10_insufficient_history_error_400(self):
        dates = pd.date_range("2026-01-01", periods=10, freq="D")
        series = [{"date": d.strftime("%Y-%m-%d"), "net_cash_flow": 1000.0} for d in dates]
        payload = {
            "forecast_date": "2026-01-11",
            "historical_series": series
        }
        response = self.client.post("/api/v1/ml/cash-flow-forecast", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("At least 30 historical daily records are required", response.json()["detail"])

    def test_11_customer_segmentation_customers_discovery(self):
        project_root = Path(__file__).resolve().parent.parent
        customers_df = pd.read_csv(project_root / "real_estate_intelligence_dataset" / "processed" / "customers.csv")
        valid_customer_ids = set(customers_df["customer_id"])

        response = self.client.get("/api/v1/ml/customer-segmentation/segments/1/customers?limit=5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 5)
        for record in data:
            self.assertIn(record["customer_id"], valid_customer_ids)
            self.assertNotIn("phone_number", record)
            self.assertNotIn("email", record)
            self.assertIn("budget_max_egp", record)
            self.assertIn("monthly_income_egp", record)
            self.assertIn("customer_tier", record)

    def test_12_customer_segmentation_customers_invalid_cluster(self):
        response = self.client.get("/api/v1/ml/customer-segmentation/segments/99/customers")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
