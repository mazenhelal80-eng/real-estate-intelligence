import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from ml.anomaly_detection.isolation_forest import detect_isolation_forest
from ml.anomaly_detection.local_outlier_factor import detect_local_outlier_factor
from ml.anomaly_detection.one_class_svm import detect_one_class_svm

data_path = project_root / "real_estate_intelligence_dataset" / "processed" / "ml_track1_property_pricing.csv"

df = pd.read_csv(data_path)

feature_cols = [
    "area_sqm", "bedrooms", "bathrooms", "floor_number",
    "base_price_egp", "expected_rent_monthly_egp", "price_per_sqm",
    "property_age", "rental_yield", "room_density", "popularity_score"
]
X = df[feature_cols]

if_flags, if_scores = detect_isolation_forest(X, contamination=0.01, random_state=42)
lof_flags, lof_scores = detect_local_outlier_factor(X, n_neighbors=20, contamination=0.01)
ocsvm_flags, ocsvm_scores = detect_one_class_svm(X, nu=0.01, kernel="rbf", gamma="scale")

results = df[[
    "unit_id", "project_id", "area_sqm", "bedrooms", "bathrooms",
    "base_price_egp", "price_per_sqm", "rental_yield", "is_outlier"
]].copy()

results["if_anomaly"] = if_flags
results["lof_anomaly"] = lof_flags
results["ocsvm_anomaly"] = ocsvm_flags
results["consensus_votes"] = if_flags + lof_flags + ocsvm_flags

total = len(df)
print("=" * 90)
print("PROPERTY / VALUATION ANOMALY DETECTION TRACK")
print("=" * 90)
print(f"Dataset:       {data_path.name}")
print(f"Total Units:   {total:,d}")
print(f"Feature Count: {len(feature_cols)} features ({', '.join(feature_cols[:4])}...)")
print("-" * 90)

print("Detection Summary Across Algorithms:")
print(f"  Isolation Forest:  {if_flags.sum():>4,d} anomalies ({(if_flags.sum() / total) * 100:.2f}%)")
print(f"  Local Outlier Fac: {lof_flags.sum():>4,d} anomalies ({(lof_flags.sum() / total) * 100:.2f}%)")
print(f"  One-Class SVM:     {ocsvm_flags.sum():>4,d} anomalies ({(ocsvm_flags.sum() / total) * 100:.2f}%)")

consensus_2 = int((results["consensus_votes"] >= 2).sum())
consensus_3 = int((results["consensus_votes"] == 3).sum())
print(f"\nConsensus Overlap:")
print(f"  Flagged by >= 2 algorithms: {consensus_2:>4,d} units ({(consensus_2 / total) * 100:.2f}%)")
print(f"  Flagged by all 3 (unanimous): {consensus_3:>4,d} units ({(consensus_3 / total) * 100:.2f}%)")

print("\nExisting Business Flag Correlation (for factual inspection):")
existing_outliers = int(results["is_outlier"].sum())
overlap_if = int(((results["if_anomaly"] == 1) & (results["is_outlier"] == True)).sum())
overlap_lof = int(((results["lof_anomaly"] == 1) & (results["is_outlier"] == True)).sum())
overlap_ocsvm = int(((results["ocsvm_anomaly"] == 1) & (results["is_outlier"] == True)).sum())
print(f"  Existing dataset 'is_outlier' flags: {existing_outliers:,d}")
print(f"  Overlap with Isolation Forest:       {overlap_if:,d} / {existing_outliers}")
print(f"  Overlap with Local Outlier Factor:   {overlap_lof:,d} / {existing_outliers}")
print(f"  Overlap with One-Class SVM:          {overlap_ocsvm:,d} / {existing_outliers}")

print("\nSample High-Consensus Property Anomalies (Flagged by >= 2 Algorithms):")
sample_anomalies = results[results["consensus_votes"] >= 2][[
    "unit_id", "project_id", "area_sqm", "base_price_egp",
    "price_per_sqm", "rental_yield", "consensus_votes"
]].head(5)
print(sample_anomalies.to_string(index=False))
print("=" * 90)
