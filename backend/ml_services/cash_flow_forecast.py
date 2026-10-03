from pathlib import Path
import pandas as pd
import numpy as np
from ml.packaging.model_packaging import load_packaged_model
from ml.forecasting.feature_engineering import create_forecasting_features

_MODEL_BUNDLE = None

def _get_bundle():
    global _MODEL_BUNDLE
    if _MODEL_BUNDLE is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        artifact_dir = project_root / "models" / "forecasting" / "cash_flow_linear_v1"
        _MODEL_BUNDLE = load_packaged_model(artifact_dir)
    return _MODEL_BUNDLE

def forecast_cash_flow(data, forecast_date=None):
    bundle = _get_bundle()
    model = bundle["model"]
    meta = bundle["metadata"]
    expected_features = meta.get("feature_order", [])

    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise TypeError("Input data must be a dict or a pandas DataFrame")

    if all(col in df.columns for col in expected_features):
        X = df[expected_features].astype(float)
        predictions = model.predict(X)
        if len(predictions) == 1:
            date_str = str(forecast_date) if forecast_date is not None else (str(df["date"].iloc[0]) if "date" in df.columns else "next_period")
            return {
                "model_name": meta.get("model_name", "cash_flow_linear_v1"),
                "model_version": meta.get("model_version", "v1"),
                "forecast_date": date_str,
                "predicted_net_cash_flow": float(predictions[0])
            }
        return {
            "model_name": meta.get("model_name", "cash_flow_linear_v1"),
            "model_version": meta.get("model_version", "v1"),
            "predicted_net_cash_flow": [float(p) for p in predictions]
        }

    if "date" in df.columns and "net_cash_flow" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
        if len(df) < 30:
            raise ValueError("At least 30 historical daily records are required to compute causal forecasting features.")
        
        if forecast_date is not None:
            f_date = pd.to_datetime(forecast_date)
            if f_date > df["date"].max():
                next_row = pd.DataFrame([{"date": f_date, "net_cash_flow": np.nan}])
                df = pd.concat([df, next_row], ignore_index=True)
        
        featured_df = create_forecasting_features(df, target_col="net_cash_flow", drop_na=False)
        target_row = featured_df.iloc[[-1]]
        
        missing = [col for col in expected_features if col not in target_row.columns or pd.isna(target_row[col].values[0])]
        if missing:
            raise ValueError(f"Unable to construct all required causal features: {missing}")

        X = target_row[expected_features].astype(float)
        pred = model.predict(X)[0]
        actual_date_str = str(target_row["date"].dt.strftime("%Y-%m-%d").values[0])

        return {
            "model_name": meta.get("model_name", "cash_flow_linear_v1"),
            "model_version": meta.get("model_version", "v1"),
            "forecast_date": actual_date_str,
            "predicted_net_cash_flow": float(pred)
        }

    raise ValueError("Input data must contain the 17 forecasting features or historical 'date' and 'net_cash_flow' series.")
