import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_xlsx = pd.read_excel(
    "Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx"
)
df_clean = df_xlsx.dropna().copy()

df_clean["ActualPostTaxProfit"] = df_clean["Profit"] - df_clean["SalesTaxOwed"]
df_clean["ActualPostTaxProfitMargin"] = (df_clean["ActualPostTaxProfit"] / df_clean["Revenue"]
)

plt.figure(figsize=(10, 5))

revenue_state = (
    df_clean.groupby("State")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))
ax1 = sns.barplot(
    data=revenue_state,
    x="State",
    y="Revenue",
    hue="State",
    palette="Blues",
    legend=False,
    edgecolor="black",
)

for container in ax1.containers:
    ax1.bar_label(container, fmt="%.0f")

plt.title("Total Revenue by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Revenue", fontsize=12)
plt.tight_layout()
plt.show()

profit_state = (
    df_clean.groupby("State")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))
ax2 = sns.barplot(
    data=profit_state,
    x="State",
    y="Profit",
    hue="State",
    palette="magma",
    legend=False,
    edgecolor="black",
)

for container in ax2.containers:
    ax2.bar_label(container, fmt="%.0f")

plt.title("Total Pre-Tax Profit by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Profit", fontsize=12)
plt.tight_layout()
plt.show()

post_profit_state = (
    df_clean.groupby("State")["ActualPostTaxProfit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))
ax3 = sns.barplot(
    data=post_profit_state,
    x="State",
    y="ActualPostTaxProfit",
    hue="State",
    palette="magma",
    legend=False,
    edgecolor="black",
)

for container in ax3.containers:
    ax3.bar_label(container, fmt="%.0f")

plt.title("Actual Post-Tax Total Profit by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("ActualPostTaxProfit", fontsize=12)
plt.tight_layout()
plt.show()

margin_state = (
    df_clean.groupby("State")["ActualPostTaxProfitMargin"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 5))
ax4 = sns.barplot(
    data=margin_state,
    x="State",
    y="ActualPostTaxProfitMargin",
    hue="State",
    palette="viridis",
    legend=False,
    edgecolor="black",
)

for container in ax4.containers:
    ax4.bar_label(container, fmt="%.2f")

plt.title("Actual Average Post-Tax Profit Margin by State", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Actual Post-Tax Profit Margin", fontsize=12)
plt.tight_layout()
plt.show()