"""
Phase 2 - Section 2.7: Profitability Analytics
Purpose: Compute corporate gross revenue, operating expenses, net profit, and profit margins.
Outputs:
  - reports/profitability_summary.csv
  - reports/monthly_profitability.csv
"""

from pathlib import Path
import pandas as pd


def compute_profitability():
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "real_estate_intelligence_dataset" / "raw"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    deals_df = pd.read_csv(raw_dir / "deals.csv")
    payments_df = pd.read_csv(raw_dir / "rent_payments.csv")
    expenses_df = pd.read_csv(raw_dir / "expenses.csv")

    # 1. Sales Revenue (Closed Deals Only)
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()
    closed_deals["deal_date"] = pd.to_datetime(closed_deals["deal_date"])
    closed_deals["year_month"] = closed_deals["deal_date"].dt.to_period("M").astype(str)
    sales_rev_total = closed_deals["deal_price_egp"].sum()

    # 2. Rental Revenue (Collected Rent Payments)
    payments_df["payment_date"] = pd.to_datetime(payments_df["payment_date"])
    payments_df["year_month"] = payments_df["payment_date"].dt.to_period("M").astype(str)
    # Rental revenue recognized from actual collected payments
    rental_rev_total = payments_df["amount_paid_egp"].sum()

    # 3. Total Expenses
    expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"])
    expenses_df["year_month"] = expenses_df["expense_date"].dt.to_period("M").astype(str)
    expenses_total = expenses_df["amount_egp"].sum()

    # Total figures
    total_rev = sales_rev_total + rental_rev_total
    net_profit = total_rev - expenses_total
    profit_margin = round((net_profit / total_rev) * 100, 2)

    summary_df = pd.DataFrame([
        {"metric": "total_sales_revenue_egp", "value": sales_rev_total},
        {"metric": "total_rental_revenue_egp", "value": rental_rev_total},
        {"metric": "gross_revenue_egp", "value": total_rev},
        {"metric": "total_operating_expenses_egp", "value": expenses_total},
        {"metric": "net_operating_profit_egp", "value": net_profit},
        {"metric": "net_profit_margin_percentage", "value": profit_margin},
        {"metric": "sales_revenue_contribution_pct", "value": round((sales_rev_total / total_rev) * 100, 2)},
        {"metric": "rental_revenue_contribution_pct", "value": round((rental_rev_total / total_rev) * 100, 2)},
        {"metric": "accounting_definition", "value": "Net Profit = (Closed Deals Sales Revenue + Collected Rental Revenue) - Total Expenses"}
    ])

    # Monthly profitability
    m_sales = closed_deals.groupby("year_month")["deal_price_egp"].sum().rename("sales_revenue_egp")
    m_rental = payments_df.groupby("year_month")["amount_paid_egp"].sum().rename("rental_revenue_egp")
    m_expenses = expenses_df.groupby("year_month")["amount_egp"].sum().rename("expenses_egp")

    all_months = sorted(list(set(m_sales.index).union(set(m_rental.index)).union(set(m_expenses.index))))
    monthly_df = pd.DataFrame({"year_month": all_months})
    monthly_df = monthly_df.merge(m_sales, on="year_month", how="left").fillna({"sales_revenue_egp": 0.0})
    monthly_df = monthly_df.merge(m_rental, on="year_month", how="left").fillna({"rental_revenue_egp": 0.0})
    monthly_df = monthly_df.merge(m_expenses, on="year_month", how="left").fillna({"expenses_egp": 0.0})

    monthly_df["total_revenue_egp"] = monthly_df["sales_revenue_egp"] + monthly_df["rental_revenue_egp"]
    monthly_df["net_profit_egp"] = monthly_df["total_revenue_egp"] - monthly_df["expenses_egp"]
    monthly_df["profit_margin_percentage"] = (
        (monthly_df["net_profit_egp"] / monthly_df["total_revenue_egp"].replace(0, pd.NA)) * 100
    ).fillna(0.0).round(2)

    summary_path = reports_dir / "profitability_summary.csv"
    monthly_path = reports_dir / "monthly_profitability.csv"

    summary_df.to_csv(summary_path, index=False, encoding="utf-8")
    monthly_df.to_csv(monthly_path, index=False, encoding="utf-8")

    print(f"-> Generated {summary_path.relative_to(project_root)}")
    print(f"-> Generated {monthly_path.relative_to(project_root)}")

    return summary_df, monthly_df


if __name__ == "__main__":
    compute_profitability()
