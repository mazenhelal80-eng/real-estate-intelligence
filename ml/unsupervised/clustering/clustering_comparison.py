import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

kmeans = KMeans(n_clusters=4, init="k-means++", n_init=10, random_state=42)
kmeans_labels = kmeans.fit_predict(X)
kmeans_score = silhouette_score(X, kmeans_labels)

hierarchical = AgglomerativeClustering(n_clusters=4, linkage="ward")
hier_labels = hierarchical.fit_predict(X)
hier_score = silhouette_score(X, hier_labels)

dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X)
dbscan_clusters = len(set(dbscan_labels) - {-1})
dbscan_noise = int((dbscan_labels == -1).sum())

dbscan_valid = dbscan_labels != -1
if dbscan_clusters > 1 and dbscan_valid.sum() > dbscan_clusters:
    dbscan_score = f"{silhouette_score(X[dbscan_valid], dbscan_labels[dbscan_valid]):.4f}"
else:
    dbscan_score = "N/A"

print("=" * 80)
print("CLUSTERING ALGORITHMS BASELINE COMPARISON")
print("=" * 80)

summary_data = [
    {
        "Algorithm": "K-Means",
        "Type": "Centroid-based (Partitioning)",
        "Requires K": "Yes",
        "Clusters Found": 4,
        "Noise Points": 0,
        "Silhouette Score": f"{kmeans_score:.4f}",
        "Cluster Shape": "Spherical / Convex"
    },
    {
        "Algorithm": "Hierarchical (Ward)",
        "Type": "Hierarchical (Agglomerative)",
        "Requires K": "Yes (cut level)",
        "Clusters Found": 4,
        "Noise Points": 0,
        "Silhouette Score": f"{hier_score:.4f}",
        "Cluster Shape": "Variance-minimizing clusters"
    },
    {
        "Algorithm": "DBSCAN",
        "Type": "Density-based",
        "Requires K": "No (eps, min_samples)",
        "Clusters Found": dbscan_clusters,
        "Noise Points": dbscan_noise,
        "Silhouette Score": dbscan_score,
        "Cluster Shape": "Arbitrary density-connected shapes"
    }
]

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("CLUSTER DISTRIBUTION PER ALGORITHM")
print("=" * 80)

print("\nK-Means Cluster Counts:")
print(pd.Series(kmeans_labels).value_counts().sort_index().to_dict())

print("\nHierarchical Cluster Counts:")
print(pd.Series(hier_labels).value_counts().sort_index().to_dict())

print("\nDBSCAN Cluster Counts (including noise -1):")
print(pd.Series(dbscan_labels).value_counts().sort_index().to_dict())
print("=" * 80)
