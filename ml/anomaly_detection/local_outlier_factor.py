import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

def detect_local_outlier_factor(X, n_neighbors=20, contamination=0.01):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LocalOutlierFactor(
        n_neighbors=n_neighbors,
        contamination=contamination,
        novelty=False
    )
    raw_preds = model.fit_predict(X_scaled)
    anomaly_flags = (raw_preds == -1).astype(int)
    scores = model.negative_outlier_factor_
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
    
    flags, scores = detect_local_outlier_factor(X, n_neighbors=20, contamination=0.01)
    
    n_anomalies = int(np.sum(flags))
    total_samples = len(flags)
    anomaly_rate = (n_anomalies / total_samples) * 100
    
    print("Algorithm: Local Outlier Factor (LOF)")
    print("Mode: Outlier Detection (novelty=False, transductive fit on current dataset)")
    print(f"Dataset: {data_path}")
    print(f"Total Samples: {total_samples:,d}")
    print(f"Detected Anomalies: {n_anomalies:,d} ({anomaly_rate:.2f}%)")
    print(f"Negative Outlier Factor Range: [{scores.min():.4f}, {scores.max():.4f}]")
    
    results = df[["unit_id", "project_id", "area_sqm", "base_price_egp", "price_per_sqm"]].copy()
    results["anomaly"] = flags
    results["lof_score"] = scores
    
    anomalous_units = results[results["anomaly"] == 1].sort_values("lof_score").head(5)
    print("\nTop 5 Most Anomalous Property Units (Lowest Local Density):")
    print(anomalous_units.to_string(index=False))
