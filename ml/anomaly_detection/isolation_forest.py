import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_isolation_forest(X, contamination=0.01, random_state=42):
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )
    raw_preds = model.fit_predict(X)
    anomaly_flags = (raw_preds == -1).astype(int)
    scores = model.decision_function(X)
    return anomaly_flags, scores

if __name__ == "__main__":
    data_path = r"real_estate_intelligence_dataset\processed\ml_track1_property_pricing.csv"
    df = pd.read_csv(data_path)
    
    feature_cols = [
        "area_sqm", "bedrooms", "bathrooms", "floor_number",
        "base_price_egp", "expected_rent_monthly_egp", "price_per_sqm",
        "property_age", "rental_yield", "room_density", "popularity_score"
    ]
    X = df[feature_cols]
    
    flags, scores = detect_isolation_forest(X, contamination=0.01, random_state=42)
    
    n_anomalies = int(np.sum(flags))
    total_samples = len(flags)
    anomaly_rate = (n_anomalies / total_samples) * 100
    
    print("Algorithm: Isolation Forest")
    print(f"Dataset: {data_path}")
    print(f"Total Samples: {total_samples:,d}")
    print(f"Detected Anomalies: {n_anomalies:,d} ({anomaly_rate:.2f}%)")
    
    results = df[["unit_id", "project_id", "area_sqm", "base_price_egp", "price_per_sqm"]].copy()
    results["anomaly"] = flags
    results["score"] = scores
    
    anomalous_units = results[results["anomaly"] == 1].sort_values("score").head(5)
    print("\nTop 5 Most Anomalous Property Units:")
    print(anomalous_units.to_string(index=False))
