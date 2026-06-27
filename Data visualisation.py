import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_xlsx = pd.read_excel("Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx")
df_clean = df_xlsx.dropna()
df_clean.info()

print(df_clean.columns.tolist())

profit_state = (
    df_clean.groupby('State')['Profit']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
plt.rcParams["figure.figsize"] = (10,3)

ax = sns.barplot(
    data=profit_state,
    x='State',
    y='Profit',
    palette='magma',
    edgecolor='black'
)

for container in ax.containers:
    ax.bar_label(container, fmt='%.0f')

#Lineplot eigenschaften sind -> palette='magma', edgecolor='black'

plt.xlabel("State", fontsize=12)
plt.ylabel("Profit", fontsize=12)

plt.title("Total Profit by State")

plt.tight_layout()
plt.show()

# Average Post-Tax Profit Margin by State

margin_state = (
    df_clean.groupby('State')['PostTaxProfitMargin']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10,5))

ax = sns.barplot(
    data=margin_state,
    x='State',
    y='PostTaxProfitMargin',
    palette='viridis',
    edgecolor='black'
)

for container in ax.containers:
    ax.bar_label(container, fmt='%.2f')

plt.title("Average Post-Tax Profit Margin by State")
plt.xlabel("State")
plt.ylabel("Post-Tax Profit Margin")

plt.tight_layout()
plt.show()

# Tax burden by state

tax = df_clean.groupby('State')[
    ['StateRate',
     'EstimatedCountyRate',
     'EstimatedCityRate']
].mean()

tax.plot(
    kind='bar',
    stacked=True,
    figsize=(10,5)
)

plt.title("Average Tax Burden by State")
plt.xticks(rotation=45)
plt.ylabel("Tax Rate")

plt.legend([
    'State Tax',
    'County Tax',
    'City Tax'
])

plt.tight_layout()
plt.show()

#Overview State Ranking 

ranking = df_clean.groupby("State").agg({
    "Profit":"sum",
    "PostTaxProfitMargin":"mean",
    "StateRate":"mean",
    "EstimatedCountyRate":"mean",
    "EstimatedCityRate":"mean"
})

print(ranking)