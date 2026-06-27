import pandas as pd

excel_path = 'data/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx'

df = pd.read_excel(excel_path)

df_clean = df.copy()
#df_clean ist die Kopie von df

df_clean = df_clean.dropna()
df_clean.info()

#Prüfung der States damit keine Fehler bei groupby() passieren 
print("States before")
print(sorted(df_clean["State"].dropna().unique()))

df_clean["State"] = df_clean["State"].str.strip()

print("States after cleaning:")
print(sorted(df_clean["State"].dropna().unique()))

print("Number of states:", df_clean["State"].nunique())

