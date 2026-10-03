import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def compute_wape(y_true, y_pred):
    denom = np.sum(np.abs(y_true))
    if denom == 0:
        return 0.0
    return (np.sum(np.abs(y_true - y_pred)) / denom) * 100

def evaluate_predictions(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    wape = compute_wape(y_true, y_pred)
    return {"MAE": mae, "RMSE": rmse, "WAPE": wape}

def evaluate_deterministic_baselines(test_df, target_col="net_cash_flow"):
    y_true = test_df[target_col].values
    
    y_naive = test_df["lag_1"].values
    y_snaive = test_df["lag_7"].values
    y_ma7 = test_df["rolling_mean_7"].values
    
    results = {
        "Naive (Last Value)": evaluate_predictions(y_true, y_naive),
        "Seasonal Naive (7-Day)": evaluate_predictions(y_true, y_snaive),
        "Moving Average (7-Day)": evaluate_predictions(y_true, y_ma7)
    }
    return results

if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        
    from ml.forecasting.time_series_preparation import build_daily_cash_flow_series
    from ml.forecasting.feature_engineering import create_forecasting_features
    from ml.forecasting.time_series_split import temporal_train_val_test_split
    
    df = create_forecasting_features(build_daily_cash_flow_series())
    train, val, test = temporal_train_val_test_split(df)
    
    baseline_metrics = evaluate_deterministic_baselines(test)
    print("Deterministic Baselines Evaluation on Holdout Test Set:")
    for name, m in baseline_metrics.items():
        print(f"  {name:<25}: MAE={m['MAE']:>14,.2f} | RMSE={m['RMSE']:>14,.2f} | WAPE={m['WAPE']:>6.2f}%")
