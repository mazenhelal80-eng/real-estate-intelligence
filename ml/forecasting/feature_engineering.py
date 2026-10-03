import pandas as pd

def create_forecasting_features(df, target_col="net_cash_flow", drop_na=True):
    data = df.sort_values("date").copy()
    target_series = data[target_col]
    
    data["lag_1"] = target_series.shift(1)
    data["lag_7"] = target_series.shift(7)
    data["lag_14"] = target_series.shift(14)
    data["lag_28"] = target_series.shift(28)
    data["lag_30"] = target_series.shift(30)
    
    shifted_target = target_series.shift(1)
    data["rolling_mean_7"] = shifted_target.rolling(window=7).mean()
    data["rolling_mean_14"] = shifted_target.rolling(window=14).mean()
    data["rolling_mean_28"] = shifted_target.rolling(window=28).mean()
    
    data["rolling_std_7"] = shifted_target.rolling(window=7).std()
    data["rolling_std_28"] = shifted_target.rolling(window=28).std()
    
    data["rolling_min_7"] = shifted_target.rolling(window=7).min()
    data["rolling_max_7"] = shifted_target.rolling(window=7).max()
    
    data["day_of_week"] = data["date"].dt.dayofweek
    data["day_of_month"] = data["date"].dt.day
    data["month"] = data["date"].dt.month
    data["quarter"] = data["date"].dt.quarter
    data["is_weekend"] = data["day_of_week"].isin([4, 5]).astype(int)
    
    if drop_na:
        data = data.dropna().reset_index(drop=True)
        
    return data

if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        
    from ml.forecasting.time_series_preparation import build_daily_cash_flow_series
    
    base_df = build_daily_cash_flow_series()
    featured_df = create_forecasting_features(base_df)
    
    print("Forecasting Feature Engineering Summary:")
    print(f"Original Records: {len(base_df):,d}")
    print(f"Records Post Burn-in Drop: {len(featured_df):,d}")
    print(f"Features Created: {featured_df.shape[1] - len(base_df.columns)}")
    print(f"Columns: {list(featured_df.columns)}")
    print("\nSample Row Features:")
    print(featured_df.iloc[0][["date", "net_cash_flow", "lag_1", "rolling_mean_7", "day_of_week"]].to_dict())
