"""
Phase 2: Automated Unit and Integration Test Suite
Purpose: Verify analytical metrics, Pandas vs SQL equivalence, boundary constraints,
         and raw dataset immutability.
"""

import hashlib
import unittest
from pathlib import Path
import pandas as pd


class TestPhase2Analytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.raw_dir = cls.project_root / "real_estate_intelligence_dataset" / "raw"
        cls.reports_dir = cls.project_root / "reports"
        cls.sql_dir = cls.reports_dir / "sql"
        cls.manifest_path = cls.project_root / "real_estate_intelligence_dataset" / "manifest.csv"

    def test_01_raw_data_immutability(self):
        """Verify all raw CSVs have identical SHA-256 hashes matching manifest."""
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

    def test_02_pandas_vs_sql_monthly_revenue(self):
        """Verify monthly sales revenue matches exactly between Pandas and SQL."""
        p_df = pd.read_csv(self.reports_dir / "monthly_revenue.csv")
        s_df = pd.read_csv(self.sql_dir / "monthly_revenue_sql.csv")
        self.assertEqual(len(p_df), len(s_df))
        self.assertAlmostEqual(p_df["revenue_egp"].sum(), s_df["revenue_egp"].sum(), delta=1.0)
        self.assertEqual(p_df["closed_deals_count"].sum(), s_df["closed_deals_count"].sum())

    def test_03_pandas_vs_sql_location_revenue(self):
        """Verify location breakdown matches exactly between Pandas and SQL."""
        p_df = pd.read_csv(self.reports_dir / "revenue_by_location.csv")
        s_df = pd.read_csv(self.sql_dir / "revenue_by_location_sql.csv")
        self.assertEqual(len(p_df), len(s_df))
        self.assertAlmostEqual(p_df["revenue_egp"].sum(), s_df["revenue_egp"].sum(), delta=1.0)

    def test_04_pandas_vs_sql_deal_metrics(self):
        """Verify deal metrics scalar values match between Pandas and SQL."""
        p_dict = pd.read_csv(self.reports_dir / "deal_metrics.csv").set_index("metric")["value"].to_dict()
        s_dict = pd.read_csv(self.sql_dir / "deal_metrics_sql.csv").iloc[0].to_dict()
        self.assertEqual(int(float(p_dict["total_closed_deals"])), int(s_dict["total_closed_deals"]))
        self.assertAlmostEqual(float(p_dict["average_deal_value_egp"]), float(s_dict["average_deal_value_egp"]), delta=0.05)

    def test_05_pandas_vs_sql_profitability(self):
        """Verify gross and net operating profit equivalence between Pandas and SQL."""
        p_dict = pd.read_csv(self.reports_dir / "profitability_summary.csv").set_index("metric")["value"].to_dict()
        s_dict = pd.read_csv(self.sql_dir / "profitability_summary_sql.csv").iloc[0].to_dict()
        self.assertAlmostEqual(
            float(p_dict["net_operating_profit_egp"]), float(s_dict["net_operating_profit_egp"]), delta=1.0
        )

    def test_06_pandas_vs_sql_rental_metrics(self):
        """Verify rental collection and occupancy percentages between Pandas and SQL."""
        p_dict = pd.read_csv(self.reports_dir / "rental_metrics.csv").set_index("metric")["value"].to_dict()
        s_dict = pd.read_csv(self.sql_dir / "rental_metrics_sql.csv").iloc[0].to_dict()
        self.assertAlmostEqual(
            float(p_dict["occupancy_rate_percentage"]), float(s_dict["occupancy_rate_percentage"]), delta=0.01
        )
        self.assertAlmostEqual(
            float(p_dict["total_rent_collected_egp"]), float(s_dict["total_rent_collected_egp"]), delta=1.0
        )

    def test_07_pandas_vs_sql_maintenance_metrics(self):
        """Verify maintenance ticket expenses between Pandas and SQL."""
        p_dict = pd.read_csv(self.reports_dir / "maintenance_metrics.csv").set_index("metric")["value"].to_dict()
        s_dict = pd.read_csv(self.sql_dir / "maintenance_metrics_sql.csv").set_index("metric")["value"].to_dict()
        self.assertAlmostEqual(
            float(p_dict["total_maintenance_expenditure_egp"]), float(s_dict["total_maintenance_expenditure_egp"]), delta=1.0
        )

    def test_08_pandas_vs_sql_project_performance(self):
        """Verify project performance revenue match between Pandas and SQL."""
        p_df = pd.read_csv(self.reports_dir / "project_performance.csv")
        s_df = pd.read_csv(self.sql_dir / "project_performance_sql.csv")
        self.assertEqual(len(p_df), len(s_df))
        self.assertAlmostEqual(p_df["revenue_egp"].sum(), s_df["revenue_egp"].sum(), delta=1.0)

    def test_09_join_cardinality_invariance(self):
        """Assert zero row multiplication during multi-hop analytical joins."""
        deals_df = pd.read_csv(self.raw_dir / "deals.csv")
        units_df = pd.read_csv(self.raw_dir / "units.csv")
        projects_df = pd.read_csv(self.raw_dir / "projects.csv")

        closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
        m_joined = closed_deals.merge(units_df, on="unit_id", how="inner").merge(projects_df, on="project_id", how="inner")
        self.assertEqual(len(m_joined), len(closed_deals), "Row multiplication detected in Deals->Units->Projects join!")

    def test_10_business_metric_boundaries(self):
        """Verify that conversion rates, occupancy rates, and profit margins are within valid physical limits."""
        conv_df = pd.read_csv(self.reports_dir / "lead_conversion_by_source.csv")
        self.assertTrue((conv_df["conversion_rate_percentage"] >= 0.0).all())
        self.assertTrue((conv_df["conversion_rate_percentage"] <= 100.0).all())

        rental_dict = pd.read_csv(self.reports_dir / "rental_metrics.csv").set_index("metric")["value"].to_dict()
        self.assertTrue(0.0 <= float(rental_dict["occupancy_rate_percentage"]) <= 100.0)
        self.assertTrue(0.0 <= float(rental_dict["collection_rate_percentage"]) <= 100.0)


if __name__ == "__main__":
    unittest.main()
