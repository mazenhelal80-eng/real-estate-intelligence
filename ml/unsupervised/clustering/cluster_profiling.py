import pandas as pd
from sklearn.cluster import KMeans

ready_path = r"real_estate_intelligence_dataset\processed\ml_ready\track3_customer_clustering_ready.csv"
raw_profile_path = r"real_estate_intelligence_dataset\processed\ml_track3_customer_segmentation.csv"

ready_df = pd.read_csv(ready_path)
profile_df = pd.read_csv(raw_profile_path)

X = ready_df.drop("customer_id", axis=1)

model = KMeans(n_clusters=4, init="k-means++", n_init=10, random_state=42)
profile_df["cluster"] = model.fit_predict(X)

num_cols = [
    "budget_min_egp",
    "budget_max_egp",
    "budget_spread_egp",
    "monthly_income_egp",
    "income_to_budget_ratio"
]

total_customers = len(profile_df)

for cluster_id in range(4):
    cluster_data = profile_df[profile_df["cluster"] == cluster_id]
    count = len(cluster_data)
    pct = (count / total_customers) * 100
    
    print(f"==========================================")
    print(f"CLUSTER {cluster_id}: {count:,d} customers ({pct:.2f}%)")
    print(f"==========================================")
    
    means = cluster_data[num_cols].mean()
    for col in num_cols:
        print(f"Average {col}: {means[col]:,.2f}")
    
    print("\nCustomer Type Distribution:")
    print(cluster_data["customer_type"].value_counts(normalize=True).round(4) * 100)
    
    print("\nCustomer Tier Distribution:")
    print(cluster_data["customer_tier"].value_counts(normalize=True).round(4) * 100)
    
    print("\nInteraction Frequency Distribution:")
    print(cluster_data["interaction_frequency"].value_counts(normalize=True).round(4) * 100)
    print("\n")
