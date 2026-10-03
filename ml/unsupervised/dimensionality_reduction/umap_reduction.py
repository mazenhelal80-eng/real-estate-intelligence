import sys
import importlib.util
import pandas as pd

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

umap_spec = importlib.util.find_spec("umap")

if umap_spec is None:
    print("UMAP Status: Dependency 'umap-learn' is not installed in the current environment.")
    print("Execution skipped: No synthetic or fabricated results generated.")
    print("Target Configuration if installed:")
    print("  Model: UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)")
    print("  Input: track3_customer_clustering_ready.csv (9,961 samples, 16 features)")
    print("  Intended output: 2D manifold embedding for exploratory visualization.")
    sys.exit(0)

import umap

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
X_umap = reducer.fit_transform(X)

print("Configuration: UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)")
print(f"Original Feature Matrix Shape: {X.shape}")
print(f"Reduced Feature Matrix Shape:  {X_umap.shape}")

print("\nSample 2D UMAP Embeddings (First 5 Customers):")
umap_sample = pd.DataFrame(X_umap[:5], columns=["UMAP 1", "UMAP 2"], index=df["customer_id"][:5])
print(umap_sample.round(4).to_string())
