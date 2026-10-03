"""
Phase 2 - Section 2.8: Rental Operations Analytics
Purpose: Analyze leasing status, occupancy, tenant payments, and rental collection efficiency.
Outputs:
  - reports/rental_metrics.csv
  - reports/rental_monthly_metrics.csv
"""

from pathlib import Path
import pandas as pd


def compute_rental_analytics():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    leases_df = pd.read_csv(raw_dir / "leases.csv")
    payments_df = pd.read_csv(raw_dir / "rent_payments.csv")
    units_df = pd.read_csv(raw_dir / "units.csv")

    total_units = len(units_df)
    total_leases = len(leases_df)
    active_leases = int((leases_df["lease_status"] == "Active").sum())
    expired_leases = int((leases_df["lease_status"] == "Expired").sum())
    terminated_leases = int((leases_df["lease_status"] == "Terminated").sum())

    # Occupied units = unique units under active lease
    active_units_count = leases_df[leases_df["lease_status"] == "Active"]["unit_id"].nunique()
    occupancy_rate = round((active_units_count / total_units) * 100, 2)

    total_due = payments_df["amount_due_egp"].sum()
    total_collected = payments_df["amount_paid_egp"].sum()
    collection_rate = round((total_collected / total_due) * 100, 2)

    paid_cnt = int((payments_df["payment_status"] == "Paid").sum())
    late_cnt = int((payments_df["payment_status"] == "Late").sum())
    partial_cnt = int((payments_df["payment_status"] == "Partial").sum())

    overall_metrics = pd.DataFrame([
        {"metric": "total_rentable_units_inventory", "value": total_units},
        {"metric": "total_leases_created", "value": total_leases},
        {"metric": "active_leases_count", "value": active_leases},
        {"metric": "expired_leases_count", "value": expired_leases},
        {"metric": "terminated_leases_count", "value": terminated_leases},
        {"metric": "active_occupied_units_count", "value": active_units_count},
        {"metric": "occupancy_rate_percentage", "value": occupancy_rate},
        {"metric": "total_rent_due_egp", "value": total_due},
        {"metric": "total_rent_collected_egp", "value": total_collected},
        {"metric": "collection_rate_percentage", "value": collection_rate},
        {"metric": "paid_payments_count", "value": paid_cnt},
        {"metric": "late_payments_count", "value": late_cnt},
        {"metric": "partial_payments_count", "value": partial_cnt},
    ])

    # Monthly rental metrics
    payments_df["due_date"] = pd.to_datetime(payments_df["due_date"])
    payments_df["year_month"] = payments_df["due_date"].dt.to_period("M").astype(str)

    monthly_rental = (
        payments_df.groupby("year_month", as_index=False)
        .agg(
            total_payments=("payment_id", "count"),
            amount_due_egp=("amount_due_egp", "sum"),
            amount_collected_egp=("amount_paid_egp", "sum"),
            paid_count=("payment_status", lambda s: (s == "Paid").sum()),
            late_count=("payment_status", lambda s: (s == "Late").sum()),
            partial_count=("payment_status", lambda s: (s == "Partial").sum()),
        )
        .sort_values("year_month")
        .reset_index(drop=True)
    )

    monthly_rental["collection_rate_percentage"] = (
        (monthly_rental["amount_collected_egp"] / monthly_rental["amount_due_egp"]) * 100
    ).round(2)

    overall_path = reports_dir / "rental_metrics.csv"
    monthly_path = reports_dir / "rental_monthly_metrics.csv"

    overall_metrics.to_csv(overall_path, index=False, encoding="utf-8")
    monthly_rental.to_csv(monthly_path, index=False, encoding="utf-8")

    print(f"-> Generated {overall_path.relative_to(project_root)}")
    print(f"-> Generated {monthly_path.relative_to(project_root)}")

    return overall_metrics, monthly_rental


if __name__ == "__main__":
    compute_rental_analytics()
