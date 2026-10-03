import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

data_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"

df = pd.read_csv(data_path)
X = df.drop("customer_id", axis=1)

pca_full = PCA(n_components=None)
pca_full.fit(X)

exp_var = pca_full.explained_variance_ratio_
cum_var = np.cumsum(exp_var)

summary_df = pd.DataFrame({
    "Component": [f"PC{i+1}" for i in range(len(exp_var))],
    "Explained Variance": exp_var,
    "Explained Variance (%)": exp_var * 100,
    "Cumulative Variance": cum_var,
    "Cumulative Variance (%)": cum_var * 100
})

print("=" * 80)
print("PCA COMPONENT AND EXPLAINED VARIANCE ANALYSIS")
print("=" * 80)
print(f"Total Input Features: {X.shape[1]}")
print(f"Total Samples:        {X.shape[0]:,d}")
print("-" * 80)
print(summary_df.round(4).to_string(index=False))
print("-" * 80)

thresholds = [0.80, 0.90, 0.95]
print("\nComponents Required for Common Variance Retention Thresholds:")
for t in thresholds:
    n_comp = int(np.argmax(cum_var >= t) + 1)
    actual_var = cum_var[n_comp - 1] * 100
    print(f"Variance >= {int(t * 100)}%: {n_comp} components (Actual: {actual_var:.2f}%)")
print("=" * 80)
