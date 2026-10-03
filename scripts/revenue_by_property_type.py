"""
Phase 2 - Section 2.3: Revenue by Property Type
Purpose: Compute sales revenue by property type (deals -> units).
Output: reports/revenue_by_property_type.csv
"""

from pathlib import Path
import pandas as pd


def compute_revenue_by_property_type():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    deals_df = pd.read_csv(raw_dir / "deals.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")

    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()
    deals_before = len(closed_deals)

    merged = closed_deals.merge(units_df[["unit_id", "property_type"]], on="unit_id", how="inner")
    if len(merged) != deals_before:
        raise ValueError(f"Join cardinality mismatch: before={deals_before}, after={len(merged)}")

    total_revenue = merged["deal_price_egp"].sum()

    prop_summary = (
        merged.groupby("property_type", as_index=False)
        .agg(
            revenue_egp=("deal_price_egp", "sum"),
            deal_count=("deal_id", "count"),
            average_deal_value_egp=("deal_price_egp", "mean"),
        )
        .sort_values("revenue_egp", ascending=False)
        .reset_index(drop=True)
    )

    prop_summary["revenue_percentage"] = (
        (prop_summary["revenue_egp"] / total_revenue) * 100
    ).round(2)
    prop_summary["average_deal_value_egp"] = prop_summary["average_deal_value_egp"].round(2)

    output_path = reports_dir / "revenue_by_property_type.csv"
    prop_summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(prop_summary)} property types)")
    return prop_summary


if __name__ == "__main__":
    compute_revenue_by_property_type()
