import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from ml.forecasting.forecasting_baseline import evaluate_predictions

def get_forecasting_models():
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "HistGradientBoosting": HistGradientBoostingRegressor(max_iter=100, random_state=42)
    }

def train_and_evaluate_models(train_df, test_df, feature_cols, target_col="net_cash_flow"):
    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    models = get_forecasting_models()
    results = {}
    predictions = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_predictions(y_test, y_pred)
        results[name] = metrics
        predictions[name] = y_pred
        
    return results, predictions, models

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
    
    feature_cols = [c for c in df.columns if c not in ["date", "sales_inflow", "rent_inflow", "total_inflow", "expense_outflow", "net_cash_flow"]]
    results, preds, _ = train_and_evaluate_models(train, val, feature_cols)
    
    print("ML Models Evaluation on Validation Set:")
    for name, m in results.items():
        print(f"  {name:<25}: MAE={m['MAE']:>14,.2f} | RMSE={m['RMSE']:>14,.2f} | WAPE={m['WAPE']:>6.2f}%")
