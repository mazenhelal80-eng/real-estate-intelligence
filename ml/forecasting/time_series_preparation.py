from pathlib import Path
import pandas as pd

def build_daily_cash_flow_series(start_date="2024-01-01", end_date="2026-09-30"):
    project_root = Path(__file__).resolve().parent.parent.parent
    processed_dir = project_root / "real_estate_intelligence_dataset" / "processed"
    
    deals_df = pd.read_csv(processed_dir / "deals.csv")
    closed_deals = deals_df[deals_df["deal_status"] == "Closed"].copy()
    closed_deals["date"] = pd.to_datetime(closed_deals["deal_date"])
    sales_daily = closed_deals.groupby("date")["deal_price_egp"].sum().rename("sales_inflow")
    
    rents_df = pd.read_csv(processed_dir / "rent_payments.csv")
    rents_df["date"] = pd.to_datetime(rents_df["payment_date"])
    rent_daily = rents_df.groupby("date")["amount_paid_egp"].sum().rename("rent_inflow")
    
    expenses_df = pd.read_csv(processed_dir / "expenses.csv")
    expenses_df["date"] = pd.to_datetime(expenses_df["expense_date"])
    expense_daily = expenses_df.groupby("date")["amount_egp"].sum().rename("expense_outflow")
    
    full_dates = pd.date_range(start=start_date, end=end_date, freq="D")
    daily_df = pd.DataFrame({"date": full_dates})
    
    daily_df = daily_df.merge(sales_daily, on="date", how="left").fillna({"sales_inflow": 0.0})
    daily_df = daily_df.merge(rent_daily, on="date", how="left").fillna({"rent_inflow": 0.0})
    daily_df = daily_df.merge(expense_daily, on="date", how="left").fillna({"expense_outflow": 0.0})
    
    daily_df["total_inflow"] = daily_df["sales_inflow"] + daily_df["rent_inflow"]
    daily_df["net_cash_flow"] = daily_df["total_inflow"] - daily_df["expense_outflow"]
    
    return daily_df

if __name__ == "__main__":
    df = build_daily_cash_flow_series()
    print("Daily Cash Flow Series Preparation Summary:")
    print(f"Date Range:     {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"Total Days:     {len(df):,d}")
    print(f"Total Inflows:  {df['total_inflow'].sum():,.2f} EGP")
    print(f"Total Outflows: {df['expense_outflow'].sum():,.2f} EGP")
    print(f"Net Cash Flow:  {df['net_cash_flow'].sum():,.2f} EGP")
    print("\nFirst 3 Days:")
    print(df.head(3).to_string(index=False))
    print("\nLast 3 Days:")
    print(df.tail(3).to_string(index=False))
