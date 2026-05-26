#DataCleaning
import pandas as pd

df_xlsx = pd.read_excel('/Users/yavuzselim/Desktop/Data Projekt/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx')

df_xlsx.info()
#394829 Zeilen 27 Spalten
df_clean = df_xlsx.dropna()
#Zeilen mit mindestens ein Fehlende Value
df_clean.info()
#394800 Zeilen 27 Spalten

anzahl_duplikate = df_clean.duplicated().sum()
print(f"Es gibt {anzahl_duplikate} doppelte Zeilen.")
#0 doppelte Zeilen

#Profite aller Staaten -> wichtig für die Zukunft
staaten_profite = df_clean.groupby('State')['Profit'].sum()

print("Hier sind die Gesamtprofite aller Staaten im Datensatz:")
print(staaten_profite)

#Umsatz aller staaten -> Im Vergleich mit Profit zu sehen wie stark die Steuern sind
umsatz = df_clean.groupby('State')['Revenue'].sum()
print("Gesamt Umsatz in den jeweiligen Staaten")
print(umsatz)

#Nexus aller Staaten
nexus = df_clean.groupby('State')['SalesTaxNoNexus'].sum()
print(nexus)

''''
date = df_clean.loc[df_clean['InvoiceYear']==2017]
anzahl_zeilen2017 = len(date)
print(f"Es gibt insgesamt {anzahl_zeilen2017} Zeilen für das Jahr 2017")
'''
#25500 Zeilen für 2016
#369300 Zeilen für 2017

etrmon = df_clean.loc[df_clean['State']== 'Washington', 'ETR'].unique()
print(etrmon)
#Montana 0
#Washington
#Wyoming
#