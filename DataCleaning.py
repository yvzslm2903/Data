import pandas as pd

df = pd.read_excel("data/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx")

df_clean = df.copy()
#df_clean ist die Kopie von df

df_clean.info()
#394829 Zeilen 27 Spalten
df_clean = df_clean.dropna()
#Zeilen mit mindestens ein Fehlende Value
df_clean.info()
#394800 Zeilen 27 Spalten

anzahl_duplikate = df_clean.duplicated().sum()
print(f"Es gibt {anzahl_duplikate} doppelte Zeilen.")
#0 doppelte Zeilen

df_clean["State"] = df_clean["State"].str.strip()

# Outlier-Behandlung für Revenue
print("Revenue vor Outlier-Behandlung:")
print(df_clean["Revenue"].describe())

lower = df_clean["Revenue"].quantile(0.01)
upper = df_clean["Revenue"].quantile(0.99)

df_clean["Revenue"] = df_clean["Revenue"].clip(lower, upper)

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

#Nexus aller Staaten
nexus = df_clean.groupby('State')['SalesTaxNoNexus'].sum().reset_index()
print(nexus)

#etrmon = df_clean.loc[df_clean['State']== 'Washington', 'ETR'].unique()
#print(etrmon)

etrmon = df_clean.loc[df_clean['State']== 'Washington', 'ETR'].unique()
print(etrmon)
#Montana 0
#Washington
#Wyoming
#

