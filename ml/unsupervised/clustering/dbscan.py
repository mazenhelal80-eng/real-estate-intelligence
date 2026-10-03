import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X)

unique_labels = set(labels)
n_clusters = len(unique_labels - {-1})
n_noise = int((labels == -1).sum())

print("Configuration: DBSCAN(eps=0.5, min_samples=5)")
print(f"Total samples: {len(labels):,d}")
print(f"Number of clusters discovered: {n_clusters}")
print(f"Number of noise points: {n_noise:,d} ({(n_noise / len(labels)) * 100:.2f}%)")

print("\nCluster Distribution:")
counts = pd.Series(labels).value_counts().sort_index()
for label, cnt in counts.items():
    name = "Noise (-1)" if label == -1 else f"Cluster {label}"
    pct = (cnt / len(labels)) * 100
    print(f"{name}: {cnt:,d} points ({pct:.2f}%)")

if n_clusters > 1 and len(unique_labels) > 1:
    valid_mask = labels != -1
    if valid_mask.sum() > n_clusters:
        score = silhouette_score(X[valid_mask], labels[valid_mask])
        print(f"\nSilhouette Score (excluding noise): {score:.4f}")
    else:
        print("\nSilhouette Score: Not enough non-noise clustered points to calculate.")
else:
    print("\nSilhouette Score: Cannot calculate (less than 2 clusters found).")
