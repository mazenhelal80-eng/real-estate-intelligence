import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

model = AgglomerativeClustering(n_clusters=4, linkage="ward")
labels = model.fit_predict(X)

print("Configuration: AgglomerativeClustering(n_clusters=4, linkage='ward')")
print(f"Total samples: {len(labels):,d}")

counts = pd.Series(labels).value_counts().sort_index()
proportions = pd.Series(labels).value_counts(normalize=True).sort_index() * 100

print("\nCluster Distribution:")
for cid in range(4):
    print(f"Cluster {cid}: {counts[cid]:,d} customers ({proportions[cid]:.2f}%)")

score = silhouette_score(X, labels)
print(f"\nSilhouette Score: {score:.4f}")
