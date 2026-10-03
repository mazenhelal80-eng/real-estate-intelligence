"""
Phase 2 - Section 2.2: Revenue by Location
Purpose: Compute sales revenue by geographic location (deals -> units -> projects).
Output: reports/revenue_by_location.csv
"""

from pathlib import Path
import pandas as pd


def compute_revenue_by_location():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    deals_df = pd.read_csv(raw_dir / "deals.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")
    projects_df = pd.read_csv(raw_dir / "projects.csv")

    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()

    # Verify join cardinalities
    deals_before = len(closed_deals)
    merged_units = closed_deals.merge(units_df[["unit_id", "project_id"]], on="unit_id", how="inner")
    if len(merged_units) != deals_before:
        raise ValueError(f"Unexpected row multiplication or drop in deals->units join: before={deals_before}, after={len(merged_units)}")

    merged_all = merged_units.merge(projects_df[["project_id", "location"]], on="project_id", how="inner")
    if len(merged_all) != deals_before:
        raise ValueError(f"Unexpected row multiplication or drop in units->projects join: before={deals_before}, after={len(merged_all)}")

    total_revenue = merged_all["deal_price_egp"].sum()

    loc_summary = (
        merged_all.groupby("location", as_index=False)
        .agg(
            revenue_egp=("deal_price_egp", "sum"),
            closed_deals_count=("deal_id", "count"),
            average_deal_value_egp=("deal_price_egp", "mean"),
        )
        .sort_values("revenue_egp", ascending=False)
        .reset_index(drop=True)
    )

    loc_summary["revenue_percentage"] = (
        (loc_summary["revenue_egp"] / total_revenue) * 100
    ).round(2)
    loc_summary["average_deal_value_egp"] = loc_summary["average_deal_value_egp"].round(2)

    output_path = reports_dir / "revenue_by_location.csv"
    loc_summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(loc_summary)} locations)")
    return loc_summary


if __name__ == "__main__":
    compute_revenue_by_location()
