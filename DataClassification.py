import DataCleaning as df
from sklearn.metrics import (accuracy_score, confusion_matrix, classification_report)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Connecting to df_clean
df_classification = df.df_clean.copy()

# Calculate the actual profit after sales tax
df_classification["ActualPostTaxProfit"] = df_classification["Profit"] - df_classification["SalesTaxOwed"]

# Calculate the actual post-tax profit margin
df_classification["ActualPostTaxProfitMargin"] = df_classification["ActualPostTaxProfit"] / df_classification["Revenue"]

margin_median = df_classification["ActualPostTaxProfitMargin"].median()
print(margin_median)
# Calculate the median of the Actualposttaxprofitmargin

df_classification["HighProfitability"] = (
    df_classification["ActualPostTaxProfitMargin"] > margin_median).astype(int)# 1 = True and 0 = False

print("Median: ", margin_median)
print(df_classification["HighProfitability"].value_counts())

# 1 = Nexus, 0 = No Nexus
# These are the 3 states with nexus 
nexus_states = ["Utah", "Washington", "Wyoming"]

df_classification["HasNexus"] = (df_classification["State"].isin(nexus_states).astype(int))


# Apply tax rates only to states with nexus
# State with Nexus = 1 -> StateRate * 1
# State without Nexus = 0 -> StateRate * 0
df_classification["ActualStateRate"] = (df_classification["StateRate"]* df_classification["HasNexus"])

df_classification["ActualCountyRate"] = (df_classification["EstimatedCountyRate"] * df_classification["HasNexus"])

df_classification["ActualCityRate"] = (df_classification["EstimatedCityRate"]* df_classification["HasNexus"])

df_classification["ActualSpecialRate"] = (df_classification["EstimatedSpecialRate"] * df_classification["HasNexus"])


# Select the features for the model
feature_columns_tax = [
    "ActualStateRate",
    "ActualCountyRate",
    "ActualCityRate",
    "ActualSpecialRate"] 


X = df_classification[feature_columns_tax]
y = df_classification["HighProfitability"]


# Split the data into 80% training data and 20% test data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20, 
    random_state=12, # mixing the Data so e.g. that you dont have only washington in training and Utah in test 
    stratify=y # Splitting 50/50 the HighProfitability and LowProfitability
)

# Create and train the logistic regression model
# The model is Weighting the 4 Taxrates how much ist affects when its changing minor Numbers like 0,498 to 0,497
fit1 = LogisticRegression(
    random_state=0,
    max_iter=1000)

# Model is training with Tax and HighProfitability
fit1.fit(X_train, y_train)

#Training done! Now Testing with the 20% Data
y_pred = fit1.predict(X_test)

# Calculate the model accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy: ", accuracy)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report( y_test, y_pred))
      
print("Intercept: ")
print(fit1.intercept_)

# - means high taxes sink the probability of HighProfitability
print("Coefficients: ")
print(fit1.coef_)


# Calculate the probability for the entire dataset
# Calculates the exact percentage chance for 1
df_classification["HighProfitabilityProbability"] = (
    fit1.predict_proba(X)[:, 1]
)

# Summarize the results by state
state_results = (
    df_classification.groupby("State")
    .agg(
        AverageProbability=("HighProfitabilityProbability","mean"),

        AverageActualPostTaxMargin=("ActualPostTaxProfitMargin","mean"),

        TotalActualPostTaxProfit=("ActualPostTaxProfit", "sum"),

        TotalProfitBeforeTax=("Profit","sum"),

        TotalSalesTaxOwed=("SalesTaxOwed","sum"),

        TotalRevenue=("Revenue","sum"),

        Transactions=("State","size")
    )
    .reset_index()
)

# Calculate the weighted actual post-tax margin
state_results["WeightedActualPostTaxMargin"] = (
    state_results["TotalActualPostTaxProfit"] / state_results["TotalRevenue"])
print(state_results)


# Convert probability and margins into percentages
state_results["AverageProbabilityPercent"] = (state_results["AverageProbability"] * 100)

state_results["AverageActualPostTaxMarginPercent"] = (state_results["AverageActualPostTaxMargin"] * 100)

state_results["WeightedActualPostTaxMarginPercent"] = (state_results["WeightedActualPostTaxMargin"] * 100)


# Sort the states by weighted profitability
state_results = state_results.sort_values(
    by="WeightedActualPostTaxMargin",
    ascending=False
)

# Create the profitability ranking table
profitability_table = state_results[
    [   "State",
        "AverageProbabilityPercent",
        "AverageActualPostTaxMarginPercent",
        "WeightedActualPostTaxMarginPercent",
        "Transactions"]].copy()

profitability_table = profitability_table.rename(
    columns={
        "AverageProbabilityPercent": "Probability %",
        "AverageActualPostTaxMarginPercent": "Avg Margin %",
        "WeightedActualPostTaxMarginPercent": "Weighted Margin %"
    }
)

print("\nPROFITABILITY RANKING")
print("-" * 85)

print(
    profitability_table.round(2).to_string(index=False)
)


# Create the financial results table
financial_table = state_results[
    [
        "State",
        "TotalRevenue",
        "TotalProfitBeforeTax",
        "TotalSalesTaxOwed",
        "TotalActualPostTaxProfit"]].copy()

financial_table = financial_table.rename(
    columns={
        "TotalRevenue": "Revenue",
        "TotalProfitBeforeTax": "Profit Before Tax",
        "TotalSalesTaxOwed": "Sales Tax",
        "TotalActualPostTaxProfit": "Post-Tax Profit"
    }
)

print("\nFINANCIAL RESULTS")
print("-" * 90)

print(
    financial_table.round(2).to_string(index=False)
)