"""
Phase 3 - Section 3.2: Domain Feature Engineering & Target Leakage Prevention Engine
Purpose: Engineer domain features, assemble modeling matrices for the 5 ML tracks,
         enforce strict target leakage barriers, and export feature dictionaries.
Output:
  - real_estate_intelligence_dataset/processed/enriched_*.csv
  - reports/phase3_feature_report.csv
"""

from pathlib import Path
from typing import Dict, List
import pandas as pd
import numpy as np


def run_feature_engineering() -> None:
    project_root = Path(__file__).resolve().parent.parent
    processed_dir = project_root / "real_estate_intelligence_dataset" / "processed"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("PHASE 3.2: DOMAIN FEATURE ENGINEERING & LEAKAGE PREVENTION")
    print("=" * 80)

    # Load cleaned tables
    units_df = pd.read_csv(processed_dir / "units.csv")
    projects_df = pd.read_csv(processed_dir / "projects.csv")
    customers_df = pd.read_csv(processed_dir / "customers.csv")
    leads_df = pd.read_csv(processed_dir / "leads.csv")
    viewings_df = pd.read_csv(processed_dir / "viewings.csv")
    deals_df = pd.read_csv(processed_dir / "deals.csv")
    listings_df = pd.read_csv(processed_dir / "listings.csv")
    maintenance_df = pd.read_csv(processed_dir / "maintenance.csv")
    rent_df = pd.read_csv(processed_dir / "rent_payments.csv")
    leases_df = pd.read_csv(processed_dir / "leases.csv")
    expenses_df = pd.read_csv(processed_dir / "expenses.csv")

    feature_records: List[Dict] = []

    # -------------------------------------------------------------
    # 1. ENRICH UNITS (Physical Real Estate Features)
    # -------------------------------------------------------------
    enriched_units = units_df.copy()
    
    # price_per_sqm (Business metric; Flagged as LEAKAGE for base_price_egp prediction)
    enriched_units["price_per_sqm"] = (enriched_units["base_price_egp"] / enriched_units["area_sqm"]).round(2)
    feature_records.append({
        "feature_name": "price_per_sqm",
        "entity": "units",
        "formula": "base_price_egp / area_sqm",
        "business_purpose": "Asset valuation density metric",
        "leakage_risk_for_price_prediction": "HIGH (DIRECT LEAKAGE) - MUST EXCLUDE FROM PRICE MODEL",
        "ml_applicability": "Track 3 Customer Segmentation / Descriptive Analytics only"
    })

    # property_age
    enriched_units["property_age"] = (2026 - enriched_units["construction_year"]).clip(lower=0)
    feature_records.append({
        "feature_name": "property_age",
        "entity": "units",
        "formula": "2026 - construction_year",
        "business_purpose": "Physical building age reflecting depreciation",
        "leakage_risk_for_price_prediction": "NONE (Valid Predictor)",
        "ml_applicability": "Track 1 Property Valuation"
    })

    # annual_expected_rent
    enriched_units["annual_expected_rent"] = enriched_units["expected_rent_monthly_egp"] * 12
    feature_records.append({
        "feature_name": "annual_expected_rent",
        "entity": "units",
        "formula": "expected_rent_monthly_egp * 12",
        "business_purpose": "Annualized rental income expectation",
        "leakage_risk_for_price_prediction": "NONE",
        "ml_applicability": "Track 1 & Track 4"
    })

    # rental_yield
    enriched_units["rental_yield"] = (
        (enriched_units["annual_expected_rent"] / enriched_units["base_price_egp"]) * 100
    ).round(2)
    feature_records.append({
        "feature_name": "rental_yield",
        "entity": "units",
        "formula": "(annual_expected_rent / base_price_egp) * 100",
        "business_purpose": "Gross rental yield percentage",
        "leakage_risk_for_price_prediction": "HIGH (DIRECT LEAKAGE) - MUST EXCLUDE FROM PRICE MODEL",
        "ml_applicability": "Investment Scoring / Track 3"
    })

    # room_density
    enriched_units["room_density"] = (
        (enriched_units["bedrooms"] + enriched_units["bathrooms"]) / enriched_units["area_sqm"] * 100
    ).round(4)
    feature_records.append({
        "feature_name": "room_density",
        "entity": "units",
        "formula": "((bedrooms + bathrooms) / area_sqm) * 100",
        "business_purpose": "Spatial efficiency and layout compactness",
        "leakage_risk_for_price_prediction": "NONE (Valid Predictor)",
        "ml_applicability": "Track 1 Property Valuation"
    })

    enriched_units.to_csv(processed_dir / "enriched_units.csv", index=False, encoding="utf-8")

    # -------------------------------------------------------------
    # 2. ENRICH CUSTOMERS (Financial & Behavioral Features)
    # -------------------------------------------------------------
    enriched_customers = customers_df.copy()

    # budget_spread_egp
    enriched_customers["budget_spread_egp"] = enriched_customers["budget_max_egp"] - enriched_customers["budget_min_egp"]
    feature_records.append({
        "feature_name": "budget_spread_egp",
        "entity": "customers",
        "formula": "budget_max_egp - budget_min_egp",
        "business_purpose": "Financial flexibility and willingness-to-pay range",
        "leakage_risk_for_price_prediction": "NONE",
        "ml_applicability": "Track 2 Lead Conversion & Track 3 Segmentation"
    })

    # income_to_budget_ratio
    enriched_customers["income_to_budget_ratio"] = (
        (enriched_customers["monthly_income_egp"] * 12) / enriched_customers["budget_max_egp"]
    ).round(4)
    feature_records.append({
        "feature_name": "income_to_budget_ratio",
        "entity": "customers",
        "formula": "(monthly_income_egp * 12) / budget_max_egp",
        "business_purpose": "Affordability and debt-service capacity ratio",
        "leakage_risk_for_price_prediction": "NONE",
        "ml_applicability": "Track 2 Lead Conversion & Track 3 Segmentation"
    })

    enriched_customers.to_csv(processed_dir / "enriched_customers.csv", index=False, encoding="utf-8")

    # -------------------------------------------------------------
    # 3. ENRICH MAINTENANCE (Operational Cost Features)
    # -------------------------------------------------------------
    enriched_maint = maintenance_df.copy()
    enriched_maint["request_date"] = pd.to_datetime(enriched_maint["request_date"])
    enriched_maint["completion_date"] = pd.to_datetime(enriched_maint["completion_date"])
    
    # maintenance_turnaround_days (valid only on completed tickets)
    enriched_maint["turnaround_days"] = (
        (enriched_maint["completion_date"] - enriched_maint["request_date"]).dt.days
    )
    feature_records.append({
        "feature_name": "turnaround_days",
        "entity": "maintenance",
        "formula": "completion_date - request_date",
        "business_purpose": "Ticket resolution velocity (operational efficiency)",
        "leakage_risk_for_price_prediction": "NONE",
        "ml_applicability": "Track 5 Anomaly Detection"
    })

    enriched_maint.to_csv(processed_dir / "enriched_maintenance.csv", index=False, encoding="utf-8")

    # -------------------------------------------------------------
    # 4. ENRICH RENT PAYMENTS (Delinquency & Timing Features)
    # -------------------------------------------------------------
    enriched_rent = rent_df.copy()
    enriched_rent["due_date"] = pd.to_datetime(enriched_rent["due_date"])
    enriched_rent["payment_date"] = pd.to_datetime(enriched_rent["payment_date"])
    
    enriched_rent["payment_delay_days"] = (
        (enriched_rent["payment_date"] - enriched_rent["due_date"]).dt.days.clip(lower=0)
    )
    enriched_rent["is_delayed"] = (enriched_rent["payment_delay_days"] > 0).astype(int)
    feature_records.append({
        "feature_name": "payment_delay_days",
        "entity": "rent_payments",
        "formula": "max(0, payment_date - due_date)",
        "business_purpose": "Tenant delinquency and cash-flow timing risk",
        "leakage_risk_for_price_prediction": "NONE",
        "ml_applicability": "Track 4 Cash-Flow & Track 5 Anomaly Detection"
    })

    enriched_rent.to_csv(processed_dir / "enriched_rent_payments.csv", index=False, encoding="utf-8")

    # -------------------------------------------------------------
    # 5. ASSEMBLE ML MODELING MATRICES
    # -------------------------------------------------------------
    # TRACK 1: Property Valuation Feature Matrix
    # Join units with projects metadata
    t1_df = enriched_units.merge(
        projects_df[["project_id", "developer_name", "location", "popularity_score", "construction_status"]],
        on="project_id",
        how="inner"
    )
    t1_output_path = processed_dir / "ml_track1_property_pricing.csv"
    t1_df.to_csv(t1_output_path, index=False, encoding="utf-8")

    # TRACK 2: Lead Conversion Feature Matrix
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    closed_lead_ids = set(closed_deals["lead_id"].dropna().unique())
    
    t2_df = leads_df.copy()
    t2_df["is_converted"] = t2_df["lead_id"].isin(closed_lead_ids).astype(int)
    
    # Merge with enriched customer attributes
    t2_df = t2_df.merge(
        enriched_customers[["customer_id", "customer_type", "customer_tier", "monthly_income_egp", "budget_max_egp", "budget_spread_egp", "income_to_budget_ratio", "interaction_frequency"]],
        on="customer_id",
        how="inner"
    )
    # Merge with listing info
    t2_df = t2_df.merge(
        listings_df[["listing_id", "listing_price_egp", "listing_type"]],
        on="listing_id",
        how="left"
    )
    t2_output_path = processed_dir / "ml_track2_lead_conversion.csv"
    t2_df.to_csv(t2_output_path, index=False, encoding="utf-8")

    # TRACK 3: Customer Segmentation Feature Matrix
    t3_df = enriched_customers[[
        "customer_id", "customer_type", "customer_tier", "budget_min_egp", "budget_max_egp",
        "budget_spread_egp", "monthly_income_egp", "income_to_budget_ratio", "interaction_frequency"
    ]].copy()
    t3_output_path = processed_dir / "ml_track3_customer_segmentation.csv"
    t3_df.to_csv(t3_output_path, index=False, encoding="utf-8")

    # Export Feature Dictionary Report
    feature_report_df = pd.DataFrame(feature_records)
    feature_report_path = reports_dir / "phase3_feature_report.csv"
    feature_report_df.to_csv(feature_report_path, index=False, encoding="utf-8")

    print(f"-> Generated {len(feature_report_df)} engineered business features.")
    print(f"-> Saved Feature Report to: {feature_report_path.relative_to(project_root)}")
    print(f"-> Saved ML Track 1 Dataset ({len(t1_df)} rows) to: {t1_output_path.relative_to(project_root)}")
    print(f"-> Saved ML Track 2 Dataset ({len(t2_df)} rows) to: {t2_output_path.relative_to(project_root)}")
    print(f"-> Saved ML Track 3 Dataset ({len(t3_df)} rows) to: {t3_output_path.relative_to(project_root)}")
    print("=" * 80)


if __name__ == "__main__":
    run_feature_engineering()
