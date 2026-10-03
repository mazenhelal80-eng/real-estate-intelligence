import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

exp_var = pca.explained_variance_ratio_
cumulative_var = np.sum(exp_var)

print("Configuration: PCA(n_components=2)")
print(f"Original Feature Matrix Shape: {X.shape}")
print(f"Reduced Feature Matrix Shape:  {X_pca.shape}")
print(f"PC1 Explained Variance Ratio:   {exp_var[0]:.4f} ({exp_var[0] * 100:.2f}%)")
print(f"PC2 Explained Variance Ratio:   {exp_var[1]:.4f} ({exp_var[1] * 100:.2f}%)")
print(f"Total 2D Explained Variance:    {cumulative_var:.4f} ({cumulative_var * 100:.2f}%)")

print("\nSample 2D PCA Projections (First 5 Customers):")
pca_sample = pd.DataFrame(X_pca[:5], columns=["PC1", "PC2"], index=df["customer_id"][:5])
print(pca_sample.round(4).to_string())
