"""
Phase 2 - Section 2.6: Agent Performance Analytics
Purpose: Compute sales activity, conversion outcomes, and commissions per agent.
Output: reports/agent_performance.csv
"""

from pathlib import Path
import pandas as pd


def compute_agent_performance():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    agents_df = pd.read_csv(raw_dir / "agents.csv")
    leads_df = pd.read_csv(raw_dir / "leads.csv")
    viewings_df = pd.read_csv(raw_dir / "viewings.csv")
    deals_df = pd.read_csv(raw_dir / "deals.csv")

    # Aggregate leads by agent
    agent_leads = leads_df.groupby("agent_id")["lead_id"].count().rename("leads_count")

    # Aggregate viewings by agent
    agent_viewings = viewings_df.groupby("agent_id")["viewing_id"].count().rename("viewings_count")

    # Aggregate deals by agent
    agent_total_deals = deals_df.groupby("agent_id")["deal_id"].count().rename("total_deals_count")
    
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"]
    agent_closed_deals = closed_deals.groupby("agent_id")["deal_id"].count().rename("closed_deals_count")
    agent_revenue = closed_deals.groupby("agent_id")["deal_price_egp"].sum().rename("revenue_egp")
    agent_commissions = closed_deals.groupby("agent_id")["commission_amount_egp"].sum().rename("commission_earned_egp")

    cancelled_deals = deals_df[deals_df["deal_status"] == "Cancelled"]
    agent_cancelled_deals = cancelled_deals.groupby("agent_id")["deal_id"].count().rename("cancelled_deals_count")

    # Combine into agents DataFrame
    perf_df = agents_df.copy()
    perf_df = perf_df.merge(agent_leads, on="agent_id", how="left").fillna({"leads_count": 0})
    perf_df = perf_df.merge(agent_viewings, on="agent_id", how="left").fillna({"viewings_count": 0})
    perf_df = perf_df.merge(agent_total_deals, on="agent_id", how="left").fillna({"total_deals_count": 0})
    perf_df = perf_df.merge(agent_closed_deals, on="agent_id", how="left").fillna({"closed_deals_count": 0})
    perf_df = perf_df.merge(agent_cancelled_deals, on="agent_id", how="left").fillna({"cancelled_deals_count": 0})
    perf_df = perf_df.merge(agent_revenue, on="agent_id", how="left").fillna({"revenue_egp": 0})
    perf_df = perf_df.merge(agent_commissions, on="agent_id", how="left").fillna({"commission_earned_egp": 0})

    perf_df["average_deal_value_egp"] = (
        perf_df["revenue_egp"] / perf_df["closed_deals_count"].replace(0, pd.NA)
    ).fillna(0.0).round(2)

    perf_df["conversion_rate_percentage"] = (
        (perf_df["closed_deals_count"] / perf_df["leads_count"].replace(0, pd.NA)) * 100
    ).fillna(0.0).round(2)

    perf_df = perf_df.sort_values("revenue_egp", ascending=False).reset_index(drop=True)

    output_path = reports_dir / "agent_performance.csv"
    perf_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"-> Generated {output_path.relative_to(project_root)} ({len(perf_df)} agents)")
    return perf_df


if __name__ == "__main__":
    compute_agent_performance()
