"""
Phase 2 - Section 2.4: Deal Analytics
Purpose: Compute aggregate and monthly deal performance metrics.
Outputs:
  - reports/deal_metrics.csv
  - reports/monthly_deal_metrics.csv
"""

from pathlib import Path
import pandas as pd


def compute_deal_metrics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    deals_df = pd.read_csv(raw_dir / "deals.csv")
    deals_df["deal_date"] = pd.to_datetime(deals_df["deal_date"])
    deals_df["year_month"] = deals_df["deal_date"].dt.to_period("M").astype(str)

    total_deals = len(deals_df)
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    cancelled_deals = deals_df[deals_df["deal_status"] == "Cancelled"]

    total_closed = len(closed_deals)
    total_cancelled = len(cancelled_deals)
    total_rev = closed_deals["deal_price_egp"].sum()
    avg_val = round(closed_deals["deal_price_egp"].mean(), 2)
    med_val = round(closed_deals["deal_price_egp"].median(), 2)
    min_val = closed_deals["deal_price_egp"].min()
    max_val = closed_deals["deal_price_egp"].max()
    cancellation_rate = round((total_cancelled / total_deals) * 100, 2)

    overall_metrics = pd.DataFrame([
        {"metric": "total_deals_created", "value": total_deals},
        {"metric": "total_closed_deals", "value": total_closed},
        {"metric": "total_cancelled_deals", "value": total_cancelled},
        {"metric": "cancellation_rate_percentage", "value": cancellation_rate},
        {"metric": "total_closed_revenue_egp", "value": total_rev},
        {"metric": "average_deal_value_egp", "value": avg_val},
        {"metric": "median_deal_value_egp", "value": med_val},
        {"metric": "min_deal_value_egp", "value": min_val},
        {"metric": "max_deal_value_egp", "value": max_val},
    ])

    # Monthly breakdown
    monthly_groups = []
    all_months = sorted(deals_df["year_month"].unique())

    for ym in all_months:
        m_deals = deals_df[deals_df["year_month"] == ym]
        m_closed = m_deals[m_deals["deal_status"] == "Closed"]
        m_cancelled = m_deals[m_deals["deal_status"] == "Cancelled"]

        m_rev = m_closed["deal_price_egp"].sum()
        m_avg = round(m_closed["deal_price_egp"].mean(), 2) if len(m_closed) > 0 else 0.0
        m_med = round(m_closed["deal_price_egp"].median(), 2) if len(m_closed) > 0 else 0.0

        monthly_groups.append({
            "year_month": ym,
            "total_deals": len(m_deals),
            "closed_deals": len(m_closed),
            "cancelled_deals": len(m_cancelled),
            "revenue_egp": m_rev,
            "average_deal_value_egp": m_avg,
            "median_deal_value_egp": m_med,
            "cancellation_rate_percentage": round((len(m_cancelled) / len(m_deals)) * 100, 2) if len(m_deals) > 0 else 0.0
        })

    monthly_df = pd.DataFrame(monthly_groups)

    overall_path = reports_dir / "deal_metrics.csv"
    monthly_path = reports_dir / "monthly_deal_metrics.csv"

    overall_metrics.to_csv(overall_path, index=False, encoding="utf-8")
    monthly_df.to_csv(monthly_path, index=False, encoding="utf-8")

    print(f"-> Generated {overall_path.relative_to(project_root)}")
    print(f"-> Generated {monthly_path.relative_to(project_root)}")

    return overall_metrics, monthly_df


if __name__ == "__main__":
    compute_deal_metrics()
