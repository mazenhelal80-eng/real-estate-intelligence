import pandas as pd

def temporal_train_val_test_split(df, val_start="2026-01-01", test_start="2026-07-01"):
    train = df[df["date"] < val_start].copy().reset_index(drop=True)
    val = df[(df["date"] >= val_start) & (df["date"] < test_start)].copy().reset_index(drop=True)
    test = df[df["date"] >= test_start].copy().reset_index(drop=True)
    return train, val, test

def generate_expanding_windows(train_df, val_df, min_train_days=365, step_days=30):
    full_df = pd.concat([train_df, val_df], ignore_index=True).sort_values("date").reset_index(drop=True)
    val_dates = set(val_df["date"])
    
    splits = []
    current_end = len(train_df)
    while current_end < len(full_df):
        next_end = min(current_end + step_days, len(full_df))
        fold_train = full_df.iloc[:current_end].copy()
        fold_val = full_df.iloc[current_end:next_end].copy()
        splits.append((fold_train, fold_val))
        current_end = next_end
        
    return splits

if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        
    from ml.forecasting.time_series_preparation import build_daily_cash_flow_series
    from ml.forecasting.feature_engineering import create_forecasting_features
    
    df = create_forecasting_features(build_daily_cash_flow_series())
    train, val, test = temporal_train_val_test_split(df)
    
    print("Temporal Split Verification:")
    print(f"Train:      {train['date'].min().strftime('%Y-%m-%d')} to {train['date'].max().strftime('%Y-%m-%d')} ({len(train):,d} days)")
    print(f"Validation: {val['date'].min().strftime('%Y-%m-%d')} to {val['date'].max().strftime('%Y-%m-%d')} ({len(val):,d} days)")
    print(f"Test:       {test['date'].min().strftime('%Y-%m-%d')} to {test['date'].max().strftime('%Y-%m-%d')} ({len(test):,d} days)")
    
    assert train["date"].max() < val["date"].min(), "Train/Val temporal overlap error!"
    assert val["date"].max() < test["date"].min(), "Val/Test temporal overlap error!"
    print("\nTemporal non-overlap assertion: PASSED")
