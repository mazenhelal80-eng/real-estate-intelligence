import importlib.util
import pandas as pd

umap_installed = importlib.util.find_spec("umap") is not None

comparison_data = [
    {
        "Method": "PCA",
        "Type": "Linear (Orthogonal Projection)",
        "Determinism": "Deterministic (Exact SVD)",
        "Variance / Distance Preservation": "Maximizes global variance",
        "Computation": "Efficient, lightweight, highly scalable",
        "Out-of-sample transform()": "Supported (native linear projection)",
        "Primary ML Use Case": "Feature reduction & pipeline preprocessing"
    },
    {
        "Method": "t-SNE",
        "Type": "Non-linear (Probabilistic Manifold)",
        "Determinism": "Stochastic (Requires fixed random_state)",
        "Variance / Distance Preservation": "Preserves local neighborhood similarities",
        "Computation": "Computationally intensive, quadratic distance scaling",
        "Out-of-sample transform()": "Not supported (non-parametric embedding)",
        "Primary ML Use Case": "Exploratory 2D/3D visualization only"
    },
    {
        "Method": "UMAP",
        "Type": "Non-linear (Fuzzy Simplicial Set)",
        "Determinism": "Stochastic (Requires fixed random_state)",
        "Variance / Distance Preservation": "Balances local neighborhoods and global structure",
        "Computation": "Generally scalable graph construction",
        "Out-of-sample transform()": "Supported (approximate projection)",
        "Primary ML Use Case": "Exploratory visualization & clustering support"
    }
]

df_comp = pd.DataFrame(comparison_data)

print("=" * 100)
print("DIMENSIONALITY REDUCTION METHODS - FACTUAL COMPARISON")
print("=" * 100)
for idx, row in df_comp.iterrows():
    print(f"\nMethod: {row['Method']}")
    print(f"  Type:                             {row['Type']}")
    print(f"  Determinism:                      {row['Determinism']}")
    print(f"  Variance / Distance Preservation: {row['Variance / Distance Preservation']}")
    print(f"  Computation:                      {row['Computation']}")
    print(f"  Out-of-sample transform():        {row['Out-of-sample transform()']}")
    print(f"  Primary ML Use Case:              {row['Primary ML Use Case']}")
    if row["Method"] == "UMAP":
        status = "Available" if umap_installed else "Not installed (umap-learn required)"
        print(f"  Current Environment Status:       {status}")

print("=" * 100)
