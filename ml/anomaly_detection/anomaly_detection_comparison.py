import pandas as pd

comparison_data = [
    {
        "Algorithm": "Isolation Forest",
        "Paradigm": "Tree-based Recursive Space Partitioning",
        "Scale Sensitivity": "Scale-invariant (monotonic split trees)",
        "Computational Profile": "Fast, parallelizable ensemble (O(n_trees * n * log(n)))",
        "Out-of-sample Inference": "Supported natively via predict() and decision_function()",
        "Outlier Decision Basis": "Fewest random splits required to isolate a point",
        "Typical Real Estate Application": "High-dimensional property and multi-attribute outlier screening"
    },
    {
        "Algorithm": "Local Outlier Factor (LOF)",
        "Paradigm": "Local Density-based Nearest Neighbors",
        "Scale Sensitivity": "Sensitive to feature scale (requires normalization for Euclidean distance)",
        "Computational Profile": "Distance-matrix intensive; scales quadratically with large sample counts",
        "Out-of-sample Inference": "Transductive in outlier mode (novelty=False); requires novelty=True for predict()",
        "Outlier Decision Basis": "Substantially lower local density compared to k-nearest neighbors",
        "Typical Real Estate Application": "Isolated sub-market clusters and local price-neighborhood discrepancies"
    },
    {
        "Algorithm": "One-Class SVM",
        "Paradigm": "Non-linear Kernel Support Vector Boundary Estimation",
        "Scale Sensitivity": "Sensitive to feature scale (requires normalization for RBF kernel)",
        "Computational Profile": "Quadratic kernel solver; computationally heavier on massive datasets",
        "Out-of-sample Inference": "Supported natively via decision_function() and predict()",
        "Outlier Decision Basis": "Distance outside the estimated high-density support boundary",
        "Typical Real Estate Application": "Non-linear luxury valuation boundaries and complex multi-modal distributions"
    }
]

df_comp = pd.DataFrame(comparison_data)

print("=" * 100)
print("ANOMALY DETECTION ALGORITHMS - FACTUAL COMPARISON")
print("=" * 100)
for idx, row in df_comp.iterrows():
    print(f"\nAlgorithm: {row['Algorithm']}")
    print(f"  Paradigm:                 {row['Paradigm']}")
    print(f"  Scale Sensitivity:        {row['Scale Sensitivity']}")
    print(f"  Computational Profile:    {row['Computational Profile']}")
    print(f"  Out-of-sample Inference:  {row['Out-of-sample Inference']}")
    print(f"  Outlier Decision Basis:   {row['Outlier Decision Basis']}")
    print(f"  Real Estate Fit:          {row['Typical Real Estate Application']}")

print("=" * 100)
