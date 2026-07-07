import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import DataCleaning

df_clean = DataCleaning.df_clean.copy()

# create nexus-adjusted profit
df_clean["PostTaxProfitIfNexus"] = df_clean["Profit"] - df_clean["SalesTaxNoNexus"]

# aggregate data by state
state_profiles = df_clean.groupby("State").agg({
    "PostTaxProfitIfNexus": "sum",
    "PostTaxProfitMargin": "mean",
    "EstimatedCombinedRate": "mean"
}).reset_index()

# select variables for clustering
cluster_variables = state_profiles[[
    "PostTaxProfitIfNexus",
    "PostTaxProfitMargin",
    "EstimatedCombinedRate"
]]

# scale variables
scaler = StandardScaler()
cluster_scaled = scaler.fit_transform(cluster_variables)

# apply k-means
kmeans = KMeans(
    n_clusters=3,
    max_iter=1000,
    random_state=12,
    n_init=10
)

state_profiles["Cluster"] = kmeans.fit_predict(cluster_scaled)

print(state_profiles)

# create centroids in original values
centroids = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=cluster_variables.columns
)

centroids["Cluster"] = centroids.index

print(centroids)

# summarize clusters
cluster_summary = state_profiles.groupby("Cluster").agg({
    "PostTaxProfitIfNexus": "mean",
    "PostTaxProfitMargin": "mean",
    "EstimatedCombinedRate": "mean",
    "State": lambda x: ", ".join(x)
}).reset_index()

print(cluster_summary)

# heatmap of scaled centroids
centroids_scaled = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=cluster_variables.columns
)

centroids_scaled["Cluster"] = centroids_scaled.index
centroids_scaled = centroids_scaled.set_index("Cluster")

plt.figure(figsize=(10, 4))

sns.heatmap(
    centroids_scaled,
    annot=True,
    cmap="BuPu",
    fmt=".2f"
)

plt.title("Cluster Profiles Based on Nexus-Adjusted Profitability")
plt.xlabel("Feature")
plt.ylabel("Cluster")
plt.tight_layout()
plt.show()