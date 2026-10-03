"""
Phase 2 - Section 2.11: Project Performance Analytics
Purpose: Compute project-level operational, revenue, cost, and profitability performance.
Output: reports/project_performance.csv
"""

from pathlib import Path
import pandas as pd


def compute_project_performance():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    projects_df = pd.read_csv(raw_dir / "projects.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")
    listings_df = pd.read_csv(raw_dir / "listings.csv")
    deals_df = pd.read_csv(raw_dir / "deals.csv")
    expenses_df = pd.read_csv(raw_dir / "expenses.csv")

    # Units per project
    units_per_prj = units_df.groupby("project_id")["unit_id"].count().rename("total_units_count")

    # Listed units per project (distinct units)
    listings_with_units = listings_df.merge(units_df[["unit_id", "project_id"]], on="unit_id", how="inner")
    listed_units_per_prj = listings_with_units.groupby("project_id")["unit_id"].nunique().rename("listed_units_count")

    # Closed deals & revenue per project
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    deals_with_units = closed_deals.merge(units_df[["unit_id", "project_id"]], on="unit_id", how="inner")
    closed_deals_cnt = deals_with_units.groupby("project_id")["deal_id"].count().rename("closed_deals_count")
    revenue_per_prj = deals_with_units.groupby("project_id")["deal_price_egp"].sum().rename("revenue_egp")

    # Expenses per project
    expenses_per_prj = expenses_df.groupby("project_id")["amount_egp"].sum().rename("total_expenses_egp")

    # Combine
    res = projects_df.copy()
    res = res.merge(units_per_prj, on="project_id", how="left").fillna({"total_units_count": 0})
    res = res.merge(listed_units_per_prj, on="project_id", how="left").fillna({"listed_units_count": 0})
    res = res.merge(closed_deals_cnt, on="project_id", how="left").fillna({"closed_deals_count": 0})
    res = res.merge(revenue_per_prj, on="project_id", how="left").fillna({"revenue_egp": 0})
    res = res.merge(expenses_per_prj, on="project_id", how="left").fillna({"total_expenses_egp": 0})

    res["average_deal_value_egp"] = (
        res["revenue_egp"] / res["closed_deals_count"].replace(0, pd.NA)
    ).fillna(0.0).round(2)

    res["net_project_profit_egp"] = res["revenue_egp"] - res["total_expenses_egp"]
    res["profit_margin_percentage"] = (
        (res["net_project_profit_egp"] / res["revenue_egp"].replace(0, pd.NA)) * 100
    ).fillna(0.0).round(2)

    res = res.sort_values("revenue_egp", ascending=False).reset_index(drop=True)

    output_path = reports_dir / "project_performance.csv"
    res.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(res)} projects)")
    return res


if __name__ == "__main__":
    compute_project_performance()
