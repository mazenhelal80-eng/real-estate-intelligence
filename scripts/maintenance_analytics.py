"""
Phase 2 - Section 2.9: Maintenance Analytics
Purpose: Analyze maintenance request volume, service categories, urgency, and cost distributions.
Outputs:
  - reports/maintenance_metrics.csv
  - reports/monthly_maintenance_metrics.csv
"""

from pathlib import Path
import pandas as pd


def compute_maintenance_analytics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    maint_df = pd.read_csv(raw_dir / "maintenance.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")
    projects_df = pd.read_csv(raw_dir / "projects.csv")

    total_tickets = len(maint_df)
    completed_tickets = int((maint_df["status"] == "Completed").sum())
    in_progress_tickets = int((maint_df["status"] == "In Progress").sum())
    scheduled_tickets = int((maint_df["status"] == "Scheduled").sum())

    total_cost = maint_df["cost_egp"].sum()
    avg_cost = round(maint_df["cost_egp"].mean(), 2)
    median_cost = round(maint_df["cost_egp"].median(), 2)

    # Breakdown by category/type
    by_type = (
        maint_df.groupby("maintenance_type", as_index=False)
        .agg(
            ticket_count=("maintenance_id", "count"),
            total_cost_egp=("cost_egp", "sum"),
            average_cost_egp=("cost_egp", "mean"),
        )
        .sort_values("total_cost_egp", ascending=False)
        .reset_index(drop=True)
    )
    by_type["cost_percentage"] = ((by_type["total_cost_egp"] / total_cost) * 100).round(2)
    by_type["average_cost_egp"] = by_type["average_cost_egp"].round(2)

    # Monthly breakdown
    maint_df["request_date"] = pd.to_datetime(maint_df["request_date"])
    maint_df["year_month"] = maint_df["request_date"].dt.to_period("M").astype(str)

    monthly_maint = (
        maint_df.groupby("year_month", as_index=False)
        .agg(
            ticket_count=("maintenance_id", "count"),
            total_cost_egp=("cost_egp", "sum"),
            average_cost_egp=("cost_egp", "mean"),
            completed_count=("status", lambda s: (s == "Completed").sum()),
            in_progress_count=("status", lambda s: (s == "In Progress").sum()),
            scheduled_count=("status", lambda s: (s == "Scheduled").sum()),
        )
        .sort_values("year_month")
        .reset_index(drop=True)
    )
    monthly_maint["average_cost_egp"] = monthly_maint["average_cost_egp"].round(2)

    # High-level summary metrics
    summary_records = [
        {"metric": "total_maintenance_tickets", "value": total_tickets},
        {"metric": "completed_tickets_count", "value": completed_tickets},
        {"metric": "in_progress_tickets_count", "value": in_progress_tickets},
        {"metric": "scheduled_tickets_count", "value": scheduled_tickets},
        {"metric": "total_maintenance_expenditure_egp", "value": total_cost},
        {"metric": "average_ticket_cost_egp", "value": avg_cost},
        {"metric": "median_ticket_cost_egp", "value": median_cost},
        {"metric": "completion_rate_percentage", "value": round((completed_tickets / total_tickets) * 100, 2)}
    ]
    summary_df = pd.DataFrame(summary_records)

    # Save outputs
    summary_path = reports_dir / "maintenance_metrics.csv"
    monthly_path = reports_dir / "monthly_maintenance_metrics.csv"

    summary_df.to_csv(summary_path, index=False, encoding="utf-8")
    monthly_maint.to_csv(monthly_path, index=False, encoding="utf-8")

    print(f"-> Generated {summary_path.relative_to(project_root)}")
    print(f"-> Generated {monthly_path.relative_to(project_root)}")

    return summary_df, monthly_maint


if __name__ == "__main__":
    compute_maintenance_analytics()
