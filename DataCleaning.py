import pandas as pd
import numpy as np


df = pd.read_excel('/Users/yavuzselim/Desktop/Data Projekt/Data/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx')

df_clean = df.copy()
#df_clean ist die Kopie von df

df_clean.info()
#394829 Zeilen 27 Spalten
df_clean = df_clean.dropna()
#Zeilen mit mindestens ein Fehlende Value
df_clean.info()
#394800 Zeilen 27 Spalten
df_clean = df_clean.reset_index(drop=True)
#Damit wird ein reset ausgeführt damit die 29 zeilen ausgeschlossen werden
 

anzahl_duplikate = df_clean.duplicated().sum()
print(f"Es gibt {anzahl_duplikate} doppelte Zeilen.")
#0 doppelte Zeilen

df_clean["Revenue_Original"] = df_clean["Revenue"].copy()

lower = df_clean["Revenue_Original"].quantile(0.01)
upper = df_clean["Revenue_Original"].quantile(0.99)

df_clean["Revenue_Clipped"] = (
    df_clean["Revenue_Original"]
    .clip(lower=lower, upper=upper)
)

print("Revenue Original:")
print(df_clean["Revenue_Original"].describe())

print("\nRevenue für Durchschnittswerte und Diagramme:")
print(df_clean["Revenue_Clipped"].describe())

df_clean["IsReturn"] = df_clean["Revenue_Original"] < 0

print("Anzahl negativer Revenue-Werte:")
print(df_clean["IsReturn"].sum())

print("\nNegative Revenue-Werte:")
print(
    df_clean.loc[
        df_clean["IsReturn"],
        "Revenue_Original"
    ].describe()
)

print(
    df_clean.nlargest(
        10,
        "Revenue_Original"
    )[["State", "InvoiceYear", "Revenue_Original", "Profit"]]
)

print(
    df_clean.nsmallest(
        10,
        "Revenue_Original"
    )[["State", "InvoiceYear", "Revenue_Original", "Profit"]]
)



print("Revenue nach Outlier-Behandlung:")
print(df_clean["Revenue"].describe())
#Ist für die Durchschnittberehcnung und Diagramme wichtig um Ausreißer zu behandeln 

'''
rows = len(df_clean[df_clean["InvoiceYear"] == 2017])
print("Die anzahl der Zeilen beträgt im jahre 2017")
print(rows)
#2016 = 25500
#2017 = 369300
'''

#Profite aller Staaten -> wichtig für die Zukunft # 3. Punkt
staaten_profite = df_clean.groupby(['State', 'InvoiceYear'])['Profit'].sum()
print("Hier sind die Gesamtprofite aller Staaten im Datensatz:")
print(staaten_profite)


#Umsatz aller staaten > Im Vergleich mit Profit zu sehen wie stark die Steuern sind # 4. Punkt
umsatz = df_clean.groupby(['State', 'InvoiceYear'])['Revenue'].sum()
print("Gesamt Umsatz in den jeweiligen Staaten")
print(umsatz)

'''
#Nexus aller Staaten
nexus = df_clean.groupby('State')['SalesTaxNoNexus'].sum().reset_index()
print(nexus)

owed = df_clean.groupby('State')['SalesTaxOwed'].sum().reset_index()
print(owed)
'''
comparison = df_clean.groupby('State').agg(
    TotalNexus = ("SalesTaxNoNexus", "sum"),
    TotalOwed = ("SalesTaxOwed", "sum")
).reset_index()

print(comparison)