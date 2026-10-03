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

data_path = project_root / "real_estate_intelligence_dataset" / "processed" / "expenses.csv"

df = pd.read_csv(data_path)

dates = pd.to_datetime(df["expense_date"])
df_features = pd.DataFrame({
    "amount_egp": df["amount_egp"],
    "expense_month": dates.dt.month,
    "expense_day_of_week": dates.dt.dayofweek
})

cat_dummies = pd.get_dummies(df["expense_category"], prefix="cat", drop_first=False, dtype=int)
X = pd.concat([df_features, cat_dummies], axis=1)

if_flags, if_scores = detect_isolation_forest(X, contamination=0.005, random_state=42)
lof_flags, lof_scores = detect_local_outlier_factor(X, n_neighbors=20, contamination=0.005)
ocsvm_flags, ocsvm_scores = detect_one_class_svm(X, nu=0.005, kernel="rbf", gamma="scale")

results = df[["expense_id", "project_id", "expense_category", "expense_date", "amount_egp", "is_anomaly"]].copy()

results["if_anomaly"] = if_flags
results["lof_anomaly"] = lof_flags
results["ocsvm_anomaly"] = ocsvm_flags
results["consensus_votes"] = if_flags + lof_flags + ocsvm_flags

total = len(df)
print("=" * 90)
print("OPERATIONAL EXPENSE ANOMALY DETECTION TRACK")
print("=" * 90)
print(f"Dataset:       {data_path.name}")
print(f"Total Records: {total:,d}")
print(f"Feature Count: {X.shape[1]} features ({', '.join(X.columns[:3])} + {len(cat_dummies.columns)} categories)")
print("-" * 90)

print("Detection Summary Across Algorithms:")
print(f"  Isolation Forest:  {if_flags.sum():>4,d} anomalies ({(if_flags.sum() / total) * 100:.2f}%)")
print(f"  Local Outlier Fac: {lof_flags.sum():>4,d} anomalies ({(lof_flags.sum() / total) * 100:.2f}%)")
print(f"  One-Class SVM:     {ocsvm_flags.sum():>4,d} anomalies ({(ocsvm_flags.sum() / total) * 100:.2f}%)")

consensus_2 = int((results["consensus_votes"] >= 2).sum())
consensus_3 = int((results["consensus_votes"] == 3).sum())
print(f"\nConsensus Overlap:")
print(f"  Flagged by >= 2 algorithms: {consensus_2:>4,d} transactions ({(consensus_2 / total) * 100:.2f}%)")
print(f"  Flagged by all 3 (unanimous): {consensus_3:>4,d} transactions ({(consensus_3 / total) * 100:.2f}%)")

print("\nExisting Business Flag Correlation (for factual inspection):")
existing_anomalies = int(results["is_anomaly"].sum())
overlap_if = int(((results["if_anomaly"] == 1) & (results["is_anomaly"] == True)).sum())
overlap_lof = int(((results["lof_anomaly"] == 1) & (results["is_anomaly"] == True)).sum())
overlap_ocsvm = int(((results["ocsvm_anomaly"] == 1) & (results["is_anomaly"] == True)).sum())
print(f"  Existing dataset 'is_anomaly' flags: {existing_anomalies:,d}")
print(f"  Overlap with Isolation Forest:       {overlap_if:,d} / {existing_anomalies}")
print(f"  Overlap with Local Outlier Factor:   {overlap_lof:,d} / {existing_anomalies}")
print(f"  Overlap with One-Class SVM:          {overlap_ocsvm:,d} / {existing_anomalies}")

print("\nSample High-Consensus Expense Anomalies (Flagged by >= 2 Algorithms):")
sample_expenses = results[results["consensus_votes"] >= 2][[
    "expense_id", "project_id", "expense_category", "expense_date",
    "amount_egp", "consensus_votes"
]].sort_values("amount_egp", ascending=False).head(5)
print(sample_expenses.to_string(index=False))
print("=" * 90)
