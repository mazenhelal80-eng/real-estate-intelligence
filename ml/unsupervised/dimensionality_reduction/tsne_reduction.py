import pandas as pd
from sklearn.manifold import TSNE

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

tsne = TSNE(n_components=2, perplexity=30.0, max_iter=1000, random_state=42, init="pca")
X_tsne = tsne.fit_transform(X)

print("Configuration: TSNE(n_components=2, perplexity=30.0, max_iter=1000, random_state=42, init='pca')")
print(f"Original Feature Matrix Shape: {X.shape}")
print(f"Reduced Feature Matrix Shape:  {X_tsne.shape}")
print(f"Kullback-Leibler Divergence:   {tsne.kl_divergence_:.4f}")

print("\nSample 2D t-SNE Embeddings (First 5 Customers):")
tsne_sample = pd.DataFrame(X_tsne[:5], columns=["t-SNE 1", "t-SNE 2"], index=df["customer_id"][:5])
print(tsne_sample.round(4).to_string())

print("\nOperational Notice:")
print("t-SNE is a non-parametric exploratory visualization method.")
print("It does not preserve global distances or provide an out-of-sample transform() mapping.")
print("It is not suitable as a direct feature transformer for production ML pipelines.")
