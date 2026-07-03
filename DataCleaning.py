import pandas as pd

file_name = "Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx"
df = pd.read_excel(file_name)

df_clean = df.copy()

df_clean.info()
# 394829 Zeilen 

anzahlduplikate = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()
print(f"Es gibt {anzahlduplikate} duplikate")
# Keine Duplikate

df_clean = df_clean.dropna().reset_index(drop = True)
# 29 Zeilen mit min. 1 Fehlenden Wert


print(df_clean['Revenue'].describe().round(2))

vorher = df_clean.shape[0]
print(vorher)

df_clean = df_clean.loc[(df_clean['Revenue'] > 0) & 
                        (df_clean['Quantity'] > 0) & 
                        (df_clean['UnitPrice'] > 0)]
# Umsätze unter 0 & Qunatity unter 0 & Unitprice unter 0 werden ausgefiltert 
# Aus Sicherheitsgründen damit keine Fehler enthalten sind

nachher = df_clean.shape[0]
print(nachher)

differenz = vorher - nachher 
print(f"Die Differenz liegt bei: {differenz}")


q_high = df_clean['Revenue'].quantile(0.999)# Oder 0.9999 absprache halten
print(df_clean['Revenue'].quantile(0.999))

df_clean = df_clean.loc[df_clean['Revenue'] < q_high].reset_index(drop=True)
# Damit werden die oberen 0,01% gelöscht um mutmaßliche Falsch abbuchungen zu eliminieren


year = df_clean[['InvoiceYear']].value_counts()
print(year)
# Jahresdiffernez an Daten


print(df_clean['Revenue'].describe().round(2))
# Zu sehen das die Standardabweichung bei Revenue wieder normal ist 
# Von 428 auf 40.45 gesunken 


print(df_clean['Revenue'].max())
# Maximal berücksichtigtes Revenue