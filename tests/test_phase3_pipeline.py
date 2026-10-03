"""
Phase 3: Automated Unit and Integration Test Suite for Data Prep & Feature Pipeline
Purpose: Assert raw data immutability, zero target leakage, missing value resolutions,
         correct train/test splits, and mathematical consistency.
"""

import hashlib
import unittest
from pathlib import Path
import numpy as np
import pandas as pd


class TestPhase3Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.raw_dir = cls.project_root / "real_estate_intelligence_dataset" / "raw"
        cls.processed_dir = cls.project_root / "real_estate_intelligence_dataset" / "processed"
        cls.ml_ready_dir = cls.processed_dir / "ml_ready"
        cls.manifest_path = cls.project_root / "real_estate_intelligence_dataset" / "manifest.csv"

    def test_01_raw_data_immutability(self):
        """Assert all raw CSVs have identical SHA-256 hashes matching manifest."""
        manifest_df = pd.read_csv(self.manifest_path)
        raw_manifest = manifest_df[manifest_df["relative_path"].str.startswith("raw/")].copy()
        for _, row in raw_manifest.iterrows():
            file_path = self.project_root / "real_estate_intelligence_dataset" / row["relative_path"]
            self.assertTrue(file_path.exists(), f"Raw file {file_path.name} missing!")
            with open(file_path, "rb") as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(
                current_hash, row["sha256_hash"],
                f"Raw dataset {row['file_name']} was unexpectedly modified!"
            )

    def test_02_customers_cleaning_resolution(self):
        """Verify customers.csv dropped exactly 39 rows with missing monthly_income_egp."""
        raw_cust = pd.read_csv(self.raw_dir / "customers.csv")
        proc_cust = pd.read_csv(self.processed_dir / "customers.csv")
        self.assertEqual(len(raw_cust), 10000)
        self.assertEqual(len(proc_cust), 9961)
        self.assertEqual(proc_cust["monthly_income_egp"].isna().sum(), 0)

    def test_03_maintenance_structural_nulls_preserved(self):
        """Verify maintenance.csv preserved structural nulls for incomplete tickets."""
        proc_maint = pd.read_csv(self.processed_dir / "maintenance.csv")
        self.assertEqual(len(proc_maint), 12000)
        self.assertEqual(proc_maint["completion_date"].isna().sum(), 2137)
        # All non-completed tickets must have NaN completion_date
        non_completed = proc_maint[proc_maint["status"] != "Completed"]
        self.assertTrue(non_completed["completion_date"].isna().all())

    def test_04_feature_engineering_math_consistency(self):
        """Verify mathematical formulas for derived unit features."""
        enr_units = pd.read_csv(self.processed_dir / "enriched_units.csv")
        
        # price_per_sqm
        expected_ppm = (enr_units["base_price_egp"] / enr_units["area_sqm"]).round(2)
        np.testing.assert_allclose(enr_units["price_per_sqm"], expected_ppm, rtol=1e-3)

        # property_age
        expected_age = (2026 - enr_units["construction_year"]).clip(lower=0)
        np.testing.assert_array_equal(enr_units["property_age"], expected_age)

        # rental_yield
        expected_yield = ((enr_units["annual_expected_rent"] / enr_units["base_price_egp"]) * 100).round(2)
        np.testing.assert_allclose(enr_units["rental_yield"], expected_yield, rtol=1e-3)

    def test_05_track1_pricing_target_leakage_barrier(self):
        """Assert target-derived features are strictly excluded from Track 1 Price Model."""
        t1_train = pd.read_csv(self.ml_ready_dir / "track1_pricing_train.csv")
        t1_test = pd.read_csv(self.ml_ready_dir / "track1_pricing_test.csv")
        
        forbidden_features = [
            "price_per_sqm", "rental_yield", "annual_expected_rent",
            "expected_rent_monthly_egp", "unit_id", "project_id", "is_outlier"
        ]
        for col in forbidden_features:
            self.assertNotIn(col, t1_train.columns, f"Target leakage detected in Track 1 Train: {col}")
            self.assertNotIn(col, t1_test.columns, f"Target leakage detected in Track 1 Test: {col}")

        # Assert target column is present
        self.assertIn("target_base_price_egp", t1_train.columns)
        self.assertIn("target_base_price_egp", t1_test.columns)

    def test_06_track2_conversion_target_leakage_barrier(self):
        """Assert post-outcome variables are strictly excluded from Track 2 Lead Conversion Model."""
        t2_train = pd.read_csv(self.ml_ready_dir / "track2_conversion_train.csv")
        t2_test = pd.read_csv(self.ml_ready_dir / "track2_conversion_test.csv")

        forbidden_features = ["deal_id", "deal_price_egp", "deal_status", "commission_amount_egp", "lead_id"]
        for col in forbidden_features:
            self.assertNotIn(col, t2_train.columns, f"Post-outcome leakage detected in Track 2 Train: {col}")
            self.assertNotIn(col, t2_test.columns, f"Post-outcome leakage detected in Track 2 Test: {col}")

        self.assertIn("target_is_converted", t2_train.columns)
        self.assertIn("target_is_converted", t2_test.columns)

    def test_07_ml_matrices_no_nans_or_infs(self):
        """Assert that transformed ML modeling matrices contain zero NaNs and zero infinite values."""
        datasets = [
            self.ml_ready_dir / "track1_pricing_train.csv",
            self.ml_ready_dir / "track1_pricing_test.csv",
            self.ml_ready_dir / "track2_conversion_train.csv",
            self.ml_ready_dir / "track2_conversion_test.csv",
            self.ml_ready_dir / "track3_customer_clustering_ready.csv"
        ]
        for ds_path in datasets:
            df = pd.read_csv(ds_path)
            # drop non-numeric IDs if present for clustering
            numeric_df = df.select_dtypes(include=[np.number])
            self.assertEqual(
                numeric_df.isna().sum().sum(), 0,
                f"NaN values found in ML dataset: {ds_path.name}"
            )
            self.assertFalse(
                np.isinf(numeric_df.values).any(),
                f"Infinite values found in ML dataset: {ds_path.name}"
            )

    def test_08_split_dimensions_and_ratios(self):
        """Verify expected 80/20 train/test split partition sizes."""
        t1_train = pd.read_csv(self.ml_ready_dir / "track1_pricing_train.csv")
        t1_test = pd.read_csv(self.ml_ready_dir / "track1_pricing_test.csv")
        self.assertEqual(len(t1_train), 4000)
        self.assertEqual(len(t1_test), 1000)

        t2_train = pd.read_csv(self.ml_ready_dir / "track2_conversion_train.csv")
        t2_test = pd.read_csv(self.ml_ready_dir / "track2_conversion_test.csv")
        self.assertEqual(len(t2_train), 47822)
        self.assertEqual(len(t2_test), 11956)


if __name__ == "__main__":
    unittest.main()
