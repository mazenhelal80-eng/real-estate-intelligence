import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from ml.forecasting.time_series_preparation import build_daily_cash_flow_series
from ml.forecasting.feature_engineering import create_forecasting_features
from ml.forecasting.time_series_split import temporal_train_val_test_split, generate_expanding_windows
from ml.forecasting.forecasting_baseline import evaluate_deterministic_baselines, evaluate_predictions
from ml.forecasting.models import train_and_evaluate_models, get_forecasting_models

def run_cash_flow_forecasting_pipeline():
    raw_df = build_daily_cash_flow_series(start_date="2024-01-01", end_date="2026-09-30")
    df = create_forecasting_features(raw_df, target_col="net_cash_flow")
    
    train_df, val_df, test_df = temporal_train_val_test_split(df)
    
    non_feature_cols = ["date", "sales_inflow", "rent_inflow", "total_inflow", "expense_outflow", "net_cash_flow"]
    feature_cols = [c for c in df.columns if c not in non_feature_cols]
    
    print("=" * 95)
    print("TIME SERIES & CASH FLOW FORECASTING PIPELINE (ONE-STEP-AHEAD ROLLING)")
    print("=" * 95)
    print(f"Historical Span:     {raw_df['date'].min().strftime('%Y-%m-%d')} to {raw_df['date'].max().strftime('%Y-%m-%d')} ({len(raw_df):,d} daily records)")
    print(f"Features Engineered: {len(feature_cols)} ({', '.join(feature_cols[:5])}...)")
    print(f"Train Partition:     {train_df['date'].min().strftime('%Y-%m-%d')} to {train_df['date'].max().strftime('%Y-%m-%d')} ({len(train_df):,d} days)")
    print(f"Validation Set:      {val_df['date'].min().strftime('%Y-%m-%d')} to {val_df['date'].max().strftime('%Y-%m-%d')} ({len(val_df):,d} days)")
    print(f"Holdout Test Set:    {test_df['date'].min().strftime('%Y-%m-%d')} to {test_df['date'].max().strftime('%Y-%m-%d')} ({len(test_df):,d} days)")
    print("-" * 95)
    
    val_baselines = evaluate_deterministic_baselines(val_df)
    val_ml_results, _, _ = train_and_evaluate_models(train_df, val_df, feature_cols)
    
    print("1. VALIDATION SET PERFORMANCE (MODEL SELECTION & TUNING CHECK):")
    print(f"{'Method / Model':<30} {'MAE (EGP)':<20} {'RMSE (EGP)':<20} {'WAPE (%)':<10}")
    print("-" * 80)
    for name, m in val_baselines.items():
        print(f"{name:<30} {m['MAE']:>16,.2f} {m['RMSE']:>19,.2f} {m['WAPE']:>9.2f}%")
    for name, m in val_ml_results.items():
        print(f"{name:<30} {m['MAE']:>16,.2f} {m['RMSE']:>19,.2f} {m['WAPE']:>9.2f}%")
    print("-" * 80)
    
    print("\n2. EXPANDING-WINDOW WALK-FORWARD VALIDATION (ON VALIDATION TIMELINE):")
    windows = generate_expanding_windows(train_df, val_df, step_days=30)
    models_dict = get_forecasting_models()
    wf_metrics = {name: {"MAE": [], "RMSE": [], "WAPE": []} for name in models_dict.keys()}
    
    for i, (f_train, f_val) in enumerate(windows):
        for name, model in models_dict.items():
            model.fit(f_train[feature_cols], f_train["net_cash_flow"])
            preds = model.predict(f_val[feature_cols])
            metrics = evaluate_predictions(f_val["net_cash_flow"].values, preds)
            wf_metrics[name]["MAE"].append(metrics["MAE"])
            wf_metrics[name]["RMSE"].append(metrics["RMSE"])
            wf_metrics[name]["WAPE"].append(metrics["WAPE"])
            
    print(f"{'Model':<25} {'Mean WF MAE (EGP)':<22} {'Mean WF RMSE (EGP)':<22} {'Mean WF WAPE (%)':<15}")
    print("-" * 85)
    for name, m in wf_metrics.items():
        print(f"{name:<25} {np.mean(m['MAE']):>18,.2f} {np.mean(m['RMSE']):>21,.2f} {np.mean(m['WAPE']):>14.2f}%")
    print("-" * 85)
    
    full_train_df = pd.concat([train_df, val_df], ignore_index=True)
    test_baselines = evaluate_deterministic_baselines(test_df)
    test_ml_results, test_preds, fitted_models = train_and_evaluate_models(full_train_df, test_df, feature_cols)
    
    print("\n3. FINAL HOLDOUT TEST SET EVALUATION (2026-07-01 to 2026-09-30):")
    print(f"{'Method / Model':<30} {'MAE (EGP)':<20} {'RMSE (EGP)':<20} {'WAPE (%)':<10}")
    print("-" * 80)
    for name, m in test_baselines.items():
        print(f"{name:<30} {m['MAE']:>16,.2f} {m['RMSE']:>19,.2f} {m['WAPE']:>9.2f}%")
    for name, m in test_ml_results.items():
        print(f"{name:<30} {m['MAE']:>16,.2f} {m['RMSE']:>19,.2f} {m['WAPE']:>9.2f}%")
    print("-" * 80)
    
    print("\n4. SAMPLE ACTUAL VS PREDICTED CASH FLOW (FIRST 7 DAYS OF TEST HORIZON):")
    forecast_sample = pd.DataFrame({
        "date": test_df["date"][:7].dt.strftime("%Y-%m-%d"),
        "actual_cash_flow": test_df["net_cash_flow"][:7],
        "naive_baseline": test_df["lag_1"][:7],
        "linear_reg": test_preds["Linear Regression"][:7],
        "random_forest": test_preds["Random Forest"][:7],
        "hist_gb": test_preds["HistGradientBoosting"][:7]
    })
    print(forecast_sample.round(2).to_string(index=False))
    print("=" * 95)
    
    return {
        "val_baselines": val_baselines,
        "val_ml": val_ml_results,
        "test_baselines": test_baselines,
        "test_ml": test_ml_results,
        "sample": forecast_sample
    }

if __name__ == "__main__":
    run_cash_flow_forecasting_pipeline()
