"""
Phase 2 - Section 2.12: Market Analytics
Purpose: Synthesize location pricing, property type liquidity, and market trends.
Output: reports/market_summary.csv
"""

from pathlib import Path
import pandas as pd


def compute_market_analytics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    units_df = pd.read_csv(raw_dir / "units.csv")
    projects_df = pd.read_csv(raw_dir / "projects.csv")
    deals_df = pd.read_csv(raw_dir / "deals.csv")

    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()

    # Join units with projects
    units_full = units_df.merge(projects_df[["project_id", "location", "project_type"]], on="project_id", how="inner")
    deals_full = closed_deals.merge(units_full[["unit_id", "location", "property_type", "area_sqm"]], on="unit_id", how="inner")

    # Group by location and property type
    market_summary = (
        deals_full.groupby(["location", "property_type"], as_index=False)
        .agg(
            closed_deals_count=("deal_id", "count"),
            total_revenue_egp=("deal_price_egp", "sum"),
            average_deal_value_egp=("deal_price_egp", "mean"),
            average_unit_area_sqm=("area_sqm", "mean"),
        )
    )

    market_summary["average_price_per_sqm_egp"] = (
        market_summary["total_revenue_egp"] / (market_summary["average_unit_area_sqm"] * market_summary["closed_deals_count"])
    ).round(2)

    total_market_rev = market_summary["total_revenue_egp"].sum()
    market_summary["market_share_percentage"] = (
        (market_summary["total_revenue_egp"] / total_market_rev) * 100
    ).round(2)

    market_summary["average_deal_value_egp"] = market_summary["average_deal_value_egp"].round(2)
    market_summary["average_unit_area_sqm"] = market_summary["average_unit_area_sqm"].round(1)

    market_summary = market_summary.sort_values("total_revenue_egp", ascending=False).reset_index(drop=True)

    output_path = reports_dir / "market_summary.csv"
    market_summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(market_summary)} segments)")
    return market_summary


if __name__ == "__main__":
    compute_market_analytics()
