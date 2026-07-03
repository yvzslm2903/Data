import pandas as pd
import DataCleaning as df
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# Verknüpft mit df_clean
df_classification = df.df_clean


margin_median = df_classification["PostTaxProfitMargin"].median()
print(margin_median)
df.df_clean["HighProfitability"] = (
    df_classification["PostTaxProfitMargin"]
    > margin_median
).astype(int)


print(df_classification["HighProfitability"].value_counts())
# Die zeilen mit Profitabilität werden aufgedeckt 
# 1 = 188692 Zeilen; 0 = 197245

feature_columns = [
    "ETR",
    "Revenue"] 
# -> Einzeln abchecken also in 2 aufteieln! weil ETR alle zusammen ist das hier ist jetzt verdoppelt  

feature_columns_tax = [
    "StateRate",
    "EstimatedCountyRate",
    "EstimatedCityRate",
    "EstimatedSpecialRate",
    "Revenue"]    


X = df_classification[feature_columns]
y = df_classification["HighProfitability"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=12,
    stratify=y
)

fit1 = LogisticRegression(
    random_state=0,
    max_iter=1000
)

fit1.fit(X_train, y_train)

y_pred = fit1.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy: ", accuracy)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report( y_test, y_pred))
      
print("Intercept: ")
print(fit1.intercept_)

print("Coefficients: ")
print(fit1.coef_)


# Wahrscheinlichkeit für das gesamte Dataset
df_classification["HighProfitabilityProbability"] = (
    fit1.predict_proba(X)[:, 1]
)

# Ergebnisse pro State zusammenfassen
state_results = (
    df_classification.groupby("State")
    .agg(
        AverageProbability=(
            "HighProfitabilityProbability",
            "mean"),

        AveragePostTaxMargin=(
            "PostTaxProfitMargin",
            "mean"),

        TotalProfit=(
            "Profit",
            "sum"),

        TotalRevenue=(
            "Revenue",
            "sum"),

        AverageETR=(
            "ETR",
            "mean"),

        Transactions=(
            "State",
            "size")).reset_index()
)

# Nach Wahrscheinlichkeit für hohe Profitabilität sortieren
state_results = state_results.sort_values(
    by="AverageProbability",
    ascending=False
)

print(state_results)


state_results["AverageProbability"] = (
    state_results["AverageProbability"] * 100
)

state_results["AveragePostTaxMargin"] = (
    state_results["AveragePostTaxMargin"] * 100
)

state_results["AverageETR"] = (
    state_results["AverageETR"] * 100
)

print(
    state_results.round({
        "AverageProbability": 2,
        "AveragePostTaxMargin": 2,
        "TotalProfit": 2,
        "TotalRevenue": 2,
        "AverageETR": 2
    })
)

print(
    state_results[
        [
            "State",
            "AverageProbability",
            "AveragePostTaxMargin",
            "TotalProfit",
            "TotalRevenue",
            "AverageETR",
            "Transactions"
        ]
    ].to_string(index=False)
)

