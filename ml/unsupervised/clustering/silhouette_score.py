import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

k_values = [2, 3, 4, 5, 6, 7, 8]

for k in k_values:
    model = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = model.fit_predict(X)
    score = silhouette_score(X, labels)
    print(f"K={k} -> Silhouette Score: {score:.4f}")
