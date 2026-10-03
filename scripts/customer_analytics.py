"""
Phase 2 - Section 2.10: Customer Analytics
Purpose: Compute customer demographic breakdown, funnel activity, and revenue contribution.
Output: reports/customer_analytics.csv
"""

from pathlib import Path
import pandas as pd


def compute_customer_analytics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    customers_df = pd.read_csv(raw_dir / "customers.csv")
    leads_df = pd.read_csv(raw_dir / "leads.csv")
    viewings_df = pd.read_csv(raw_dir / "viewings.csv")
    deals_df = pd.read_csv(raw_dir / "deals.csv")

    total_customers = len(customers_df)

    # Activity mapping
    cust_with_leads = set(leads_df["customer_id"].dropna().unique())
    cust_with_viewings = set(viewings_df["customer_id"].dropna().unique())
    
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    cust_with_closed_deals = set(closed_deals["customer_id"].dropna().unique())

    # Revenue by customer type
    closed_with_cust = closed_deals.merge(customers_df[["customer_id", "customer_type", "customer_tier"]], on="customer_id", how="inner")
    rev_by_type = closed_with_cust.groupby("customer_type")["deal_price_egp"].sum()

    records = []

    # Overall Funnel
    records.append({"category": "Funnel Overview", "segment": "Total Registered Customers", "count": total_customers, "percentage": 100.0, "revenue_egp": closed_deals["deal_price_egp"].sum()})
    records.append({"category": "Funnel Overview", "segment": "Customers with Inquiries (Leads)", "count": len(cust_with_leads), "percentage": round((len(cust_with_leads) / total_customers) * 100, 2), "revenue_egp": 0.0})
    records.append({"category": "Funnel Overview", "segment": "Customers with Viewings", "count": len(cust_with_viewings), "percentage": round((len(cust_with_viewings) / total_customers) * 100, 2), "revenue_egp": 0.0})
    records.append({"category": "Funnel Overview", "segment": "Customers with Closed Deals", "count": len(cust_with_closed_deals), "percentage": round((len(cust_with_closed_deals) / total_customers) * 100, 2), "revenue_egp": closed_deals["deal_price_egp"].sum()})

    # Customer Type Breakdown
    type_counts = customers_df["customer_type"].value_counts()
    for ctype, cnt in type_counts.items():
        c_rev = rev_by_type.get(ctype, 0.0)
        records.append({
            "category": "Customer Type Breakdown",
            "segment": ctype,
            "count": int(cnt),
            "percentage": round((cnt / total_customers) * 100, 2),
            "revenue_egp": float(c_rev)
        })

    # Customer Tier Breakdown
    tier_counts = customers_df["customer_tier"].value_counts()
    rev_by_tier = closed_with_cust.groupby("customer_tier")["deal_price_egp"].sum()
    for tier, cnt in tier_counts.items():
        t_rev = rev_by_tier.get(tier, 0.0)
        records.append({
            "category": "Customer Tier Breakdown",
            "segment": tier,
            "count": int(cnt),
            "percentage": round((cnt / total_customers) * 100, 2),
            "revenue_egp": float(t_rev)
        })

    # Interaction Frequency
    freq_counts = customers_df["interaction_frequency"].value_counts()
    for freq, cnt in freq_counts.items():
        records.append({
            "category": "Interaction Frequency",
            "segment": freq,
            "count": int(cnt),
            "percentage": round((cnt / total_customers) * 100, 2),
            "revenue_egp": 0.0
        })

    cust_analytics_df = pd.DataFrame(records)
    output_path = reports_dir / "customer_analytics.csv"
    cust_analytics_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)}")
    return cust_analytics_df


if __name__ == "__main__":
    compute_customer_analytics()
