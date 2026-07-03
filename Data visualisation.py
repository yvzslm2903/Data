import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_xlsx = pd.read_excel("data/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx")
df_clean = df_xlsx.dropna().copy()

df_clean.info()
print("\nVerfügbare Spalten:")
print(df_clean.columns.tolist())
print("-" * 50)



#Total Profit by State

profit_state = (
    df_clean.groupby('State')['Profit']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))  

ax1 = sns.barplot(
    data=profit_state,
    x='State',
    y='Profit',
    hue='State',             
    palette='magma',
    legend=False,
    edgecolor='black'
)

for container in ax1.containers:
    ax1.bar_label(container, fmt='%.0f')

plt.xlabel("State", fontsize=12)
plt.ylabel("Profit", fontsize=12)
plt.title("Total Profit by State", fontsize=14)
plt.tight_layout()
plt.show()  


#Total Revenue by State
revenue_state = (
    df_clean.groupby("State")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5)) 

ax2 = sns.barplot(
    data=revenue_state,
    x="State",
    y="Revenue",
    hue="State",
    palette="Blues",
    legend=False,
    edgecolor="black"
)

for container in ax2.containers:
    ax2.bar_label(container, fmt="%.0f")

plt.title("Total Revenue by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Revenue", fontsize=12)
plt.tight_layout()
plt.show()



#Average Post-Tax Profit Margin by State

margin_state = (
    df_clean.groupby('State')['PostTaxProfitMargin']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))  # WICHTIG: Neues Fenster für Grafik 3

ax3 = sns.barplot(
    data=margin_state,
    x='State',
    y='PostTaxProfitMargin',
    hue='State',
    palette='viridis',
    legend=False,
    edgecolor='black'
)

for container in ax3.containers:
    ax3.bar_label(container, fmt='%.2f')

plt.title("Average Post-Tax Profit Margin by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Post-Tax Profit Margin", fontsize=12)
plt.tight_layout()
plt.show()


#Tax Burden by State

df_clean["TotalTaxRate"] = (
    df_clean["StateRate"]
    + df_clean["EstimatedCountyRate"]
    + df_clean["EstimatedCityRate"]
)

tax_state = (
    df_clean.groupby("State")["TotalTaxRate"]
    .mean()
    .sort_values()
    .reset_index()
)

plt.figure(figsize=(10, 5))  

ax4 = sns.barplot(
    data=tax_state,
    x="State",
    y="TotalTaxRate",
    hue="State",
    palette="rocket",
    legend=False,
    edgecolor="black"
)

for container in ax4.containers:
    ax4.bar_label(container, fmt="%.3f")

plt.title("Average Total Tax Rate by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Average Tax Rate", fontsize=12)
plt.tight_layout()
plt.show()


#Overview State Ranking 
ranking = df_clean.groupby("State").agg({
    "Revenue": "sum",
    "Profit": "sum",
    "PostTaxProfitMargin": "mean",
    "TotalTaxRate": "mean"
})


ranking["RevenueScore"] = (ranking["Revenue"] - ranking["Revenue"].min()) / (ranking["Revenue"].max() - ranking["Revenue"].min())
ranking["ProfitScore"] = (ranking["Profit"] - ranking["Profit"].min()) / (ranking["Profit"].max() - ranking["Profit"].min())
ranking["MarginScore"] = (ranking["PostTaxProfitMargin"] - ranking["PostTaxProfitMargin"].min()) / (ranking["PostTaxProfitMargin"].max() - ranking["PostTaxProfitMargin"].min())


ranking["TaxScore"] = 1 - ((ranking["TotalTaxRate"] - ranking["TotalTaxRate"].min()) / (ranking["TotalTaxRate"].max() - ranking["TotalTaxRate"].min())) 

ranking["OverallScore"] = (
    ranking["RevenueScore"]
    + ranking["ProfitScore"]
    + ranking["MarginScore"]
    + ranking["TaxScore"]
) / 4

ranking = ranking.sort_values("OverallScore", ascending=False).reset_index()

plt.figure(figsize=(10, 5))  

ax5 = sns.barplot(
    data=ranking,
    x="State",
    y="OverallScore",
    hue="State",
    palette="viridis",
    legend=False,
    edgecolor="black"
)

for container in ax5.containers:
    ax5.bar_label(container, fmt="%.2f")

plt.title("Overall State Performance Score", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Overall Score", fontsize=12)
plt.tight_layout()
plt.show()


print("\n--- TOP OPERATING STATES FOR TRINA ---")
print(ranking[["State", "OverallScore", "Revenue", "Profit"]].to_string(index=False))