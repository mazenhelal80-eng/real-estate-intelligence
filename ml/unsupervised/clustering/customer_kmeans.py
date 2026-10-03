

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def run_customer_kmeans_baseline() -> None:
    # 1. Define dataset path
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    data_path = (
        project_root
        / "real_estate_intelligence_dataset"
        / "processed"
        / "ml_ready"
        / "track3_customer_clustering_ready.csv"
    )

    assert data_path.exists(), f"Dataset not found: {data_path}"

    # 2. Load preprocessed ML-ready dataset
    df = pd.read_csv(data_path)
    total_samples, total_columns = df.shape

    print("=" * 80)
    print("BASELINE K-MEANS CLUSTERING (CUSTOMER SEGMENTATION)")
    print("=" * 80)
    print(f"Loaded dataset: {data_path.name}")
    print(f"Total Customer Records: {total_samples:,d} | Total Columns: {total_columns}")

    # 3. Separate identifier (customer_id) from predictor feature matrix (X)
    id_col = "customer_id"
    assert id_col in df.columns, f"Expected identifier column '{id_col}' in dataset"

    customer_ids = df[id_col]
    X = df.drop(columns=[id_col])

    # Validation checks on input matrix
    assert id_col not in X.columns, "Identifier leakage in feature matrix X!"
    assert X.shape == (total_samples, 16), f"Expected shape ({total_samples}, 16), got {X.shape}"
    assert X.isna().sum().sum() == 0, "NaN values detected in feature matrix X!"
    assert np.all(np.isfinite(X.values)), "Infinite values detected in feature matrix X!"

    print(f"Feature Matrix X Shape: {X.shape} (Excluded '{id_col}')")
    print(f"Features: {list(X.columns)}")

    # 4. Initialize and fit baseline K-Means model
    # Note: K=4 is an initial baseline configuration.
    # Proper cluster number selection (Elbow/Silhouette) will be conducted separately.
    n_clusters = 4
    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=10,
        random_state=42
    )
    kmeans.fit(X)

    # 5. Extract assignments and metrics
    cluster_labels = kmeans.labels_
    inertia = kmeans.inertia_
    centroids = kmeans.cluster_centers_

    # Assertions on outputs
    assert len(cluster_labels) == total_samples, "Cluster labels length mismatch!"
    assert set(cluster_labels) == set(range(n_clusters)), "Unexpected cluster labels generated!"
    assert centroids.shape == (n_clusters, X.shape[1]), f"Centroid shape mismatch: {centroids.shape}"
    assert np.isfinite(inertia) and inertia > 0, "Invalid inertia value!"

    print("\n" + "-" * 40)
    print("MODEL CONFIGURATION")
    print("-" * 40)
    print(f"Algorithm:           K-Means (sklearn.cluster.KMeans)")
    print(f"n_clusters:          {n_clusters} (Temporary educational baseline)")
    print(f"init:                k-means++")
    print(f"n_init:              10")
    print(f"random_state:        42")

    print("\n" + "-" * 40)
    print("CLUSTERING RESULTS")
    print("-" * 40)
    print(f"Inertia (WCSS):      {inertia:,.2f}")
    print(f"Centroids Shape:     {centroids.shape} ({centroids.shape[0]} clusters × {centroids.shape[1]} features)")

    # 6. Cluster size and proportion distribution
    cluster_series = pd.Series(cluster_labels, name="cluster")
    counts = cluster_series.value_counts().sort_index()
    proportions = cluster_series.value_counts(normalize=True).sort_index() * 100

    print("\nCluster Size & Proportion Distribution:")
    print(f"{'Cluster':<10} {'Customer Count':<18} {'Proportion (%)':<15}")
    print("-" * 45)
    for cluster_id in range(n_clusters):
        cnt = counts[cluster_id]
        prop = proportions[cluster_id]
        print(f"Cluster {cluster_id:<2} {cnt:>8,d} customers     {prop:>8.2f}%")
    print("-" * 45)
    print(f"Total:     {total_samples:>8,d} customers     100.00%")

    # 7. Display Centroids mapped to features
    centroids_df = pd.DataFrame(centroids, columns=X.columns, index=[f"Cluster {i}" for i in range(n_clusters)])
    print("\n" + "-" * 40)
    print("CLUSTER CENTROIDS (Mean Standardized Feature Values)")
    print("-" * 40)
    print(centroids_df.round(3).to_string())
    print("=" * 80)


if __name__ == "__main__":
    run_customer_kmeans_baseline()
