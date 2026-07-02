import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ==========================================================
# TEMPORÄR: eigenes Cleaning, damit dieses Skript allein läuft.
# Beim Zusammenführen ins finale Notebook wird dieser Block
# durch Yavuz' DataCleaning.py ersetzt!
# ==========================================================
file_name = "Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx"
df = pd.read_excel(file_name)

df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna().reset_index(drop=True)
df_clean = df_clean.loc[(df_clean['Revenue'] > 0) &
                        (df_clean['Quantity'] > 0) &
                        (df_clean['UnitPrice'] > 0)]
q_high = df_clean['Revenue'].quantile(0.999)
df_clean = df_clean.loc[df_clean['Revenue'] < q_high].reset_index(drop=True)
df_clean['State'] = df_clean['State'].str.strip()

print(df_clean.shape)

# --- Schritt 1: Spalten auswählen (State kategorial + vier Steuersätze) ---
short = df_clean[["State",
                  "StateRate",
                  "EstimatedCountyRate",
                  "EstimatedCityRate",
                  "EstimatedSpecialRate"]]

# --- Schritt 2: Kategoriale Spalte in Dummy-Variablen umwandeln (wie Vorlesung) ---
short_dummys = pd.get_dummies(short)
print(short_dummys.columns.tolist())

# --- Schritt 3: K-Means Clustering (Parameter wie in der Vorlesung) ---
kmeans = KMeans(n_clusters=4, max_iter=1000, random_state=12)
kmeans.fit(short_dummys)
df_clean["Cluster"] = kmeans.labels_

# Centroïden in einen DataFrame packen
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=short_dummys.columns)
print(centroids.round(3))
print(df_clean["Cluster"].value_counts())

# --- Schritt 4: Heatmap der Cluster-Profile (wie Vorlesung, Folie 28) ---
plt.rcParams["figure.figsize"] = (10, 4)
sns.heatmap(centroids, annot=True, cmap="BuPu", fmt=".3f")
plt.title("Steuerprofil und Bundesstaat je Cluster")
plt.xlabel("Merkmal")
plt.ylabel("Cluster")
plt.tight_layout()
plt.show()

# Interpretation Heatmap:
# Jede Cluster-Zeile wird von einem Bundesstaat dominiert (dunkle Zelle bei den State-Spalten).
# Cluster 3 (Montana) hat bei allen Steuersätzen den Wert 0 -> steuerfreie Zone.
# Cluster 0 (Washington) hat die höchste City-Steuer.
# Das Clustering trennt die Staaten also klar nach ihrer Steuerbelastung.

# --- Schritt 5: Bar-Chart der Nach-Steuer-Marge je Cluster (wie Vorlesung, Folie 26) ---
plt.figure()
df_clean.groupby("Cluster")["PostTaxProfitMargin"].mean().plot(kind="bar")
plt.title("Durchschnittliche Nach-Steuer-Marge je Cluster")
plt.xlabel("Cluster")
plt.ylabel("Ø Post-Tax Profit Margin")
plt.tight_layout()
plt.show()

# Interpretation Bar-Chart:
# Es zeigt sich ein klarer Zusammenhang zwischen Steuerlast und Profitabilität:
# Cluster 3 (Montana, steuerfrei) erreicht mit ~14% die höchste Nach-Steuer-Marge,
# Cluster 0 (Washington, höchste Steuer) mit ~4,8% die niedrigste.
# Für Trina bedeutet das: Bundesstaaten mit geringer Steuerlast sind deutlich
# profitabler und sollten bei einer Expansion priorisiert werden.