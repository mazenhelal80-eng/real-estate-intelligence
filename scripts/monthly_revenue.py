"""
Phase 2 - Section 2.1: Monthly Revenue Analytics
Purpose: Compute chronological monthly sales revenue from closed deals.
Output: reports/monthly_revenue.csv
"""

from pathlib import Path
import pandas as pd


def compute_monthly_revenue():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    deals_path = raw_dir / "deals.csv"
    deals_df = pd.read_csv(deals_path)

    # Validate required columns
    required_cols = ["deal_id", "deal_date", "deal_status", "deal_price_egp"]
    for col in required_cols:
        if col not in deals_df.columns:
            raise ValueError(f"Missing required column '{col}' in deals.csv")

    # Filter closed deals only (cancelled deals must not be counted as sales revenue)
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()
    closed_deals["deal_date"] = pd.to_datetime(closed_deals["deal_date"])
    closed_deals["year_month"] = closed_deals["deal_date"].dt.to_period("M").astype(str)

    monthly_rev = (
        closed_deals.groupby("year_month", as_index=False)
        .agg(
            revenue_egp=("deal_price_egp", "sum"),
            closed_deals_count=("deal_id", "count"),
            average_deal_value_egp=("deal_price_egp", "mean"),
            median_deal_value_egp=("deal_price_egp", "median"),
            min_deal_value_egp=("deal_price_egp", "min"),
            max_deal_value_egp=("deal_price_egp", "max"),
        )
        .sort_values("year_month")
        .reset_index(drop=True)
    )

    # Round floating values for clean reporting
    monthly_rev["average_deal_value_egp"] = monthly_rev["average_deal_value_egp"].round(2)
    monthly_rev["median_deal_value_egp"] = monthly_rev["median_deal_value_egp"].round(2)

    output_path = reports_dir / "monthly_revenue.csv"
    monthly_rev.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(monthly_rev)} months)")
    return monthly_rev


if __name__ == "__main__":
    compute_monthly_revenue()
