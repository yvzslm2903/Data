import pandas as pd

file_name = "Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx"
df = pd.read_excel(file_name)

# Create a copy of the original dataset for cleaning
df_clean = df.copy()

# Display general information about the dataset
df_clean.info()

duplicated = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()

print(f"There are {duplicated} duplicate rows")
df_clean = df_clean.dropna().reset_index(drop=True)

# Display descriptive statistics for Revenue before outlier removal
print(df_clean["Revenue"].describe().round(2))

# Remove unnecessary spaces from the State column
df_clean["State"] = df_clean["State"].str.strip()

# Calculate the lower and upper revenue limits
q_low = df_clean["Revenue"].quantile(0.001)
q_high = df_clean["Revenue"].quantile(0.999)

print(q_high)
print(q_low)

# Remove the lowest and highest 0.1% of revenue values
# to reduce the influence of extreme transactions
df_clean = df_clean.loc[
    (df_clean["Revenue"] <= q_high) &
    (df_clean["Revenue"] >= q_low)
].reset_index(drop=True)

year = df_clean[["InvoiceYear"]].value_counts()
print(year)
# Show the years of transaction for knowledge

print(df_clean["Revenue"].describe().round(2))
# The standard deviation of Revenue should be decreased
# because extreme values were removed
