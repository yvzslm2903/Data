import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_excel("Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx")
df_clean = df.dropna()
jahres_umsatz = df_clean.groupby('InvoiceYear')['Revenue'].sum().reset_index()

# 2. WICHTIG: Das Jahr in ein echtes Datum umwandeln und als Index setzen
# Macht aus 2015 -> 2015-01-01
jahres_umsatz['InvoiceYear'] = pd.to_datetime(jahres_umsatz['InvoiceYear'], format='%Y')
jahres_umsatz.set_index('InvoiceYear', inplace=True)

# 3. Dem Index die jährliche Frequenz zuweisen
jahres_umsatz = jahres_umsatz.asfreq('YS')

# 4. Modell anpassen – Jetzt explizit mit Trend (z.B. additiv), da Trina wächst!
model = ExponentialSmoothing(jahres_umsatz['Revenue'], trend='add', seasonal=None)
model_fit = model.fit()

# 5. Vorhersage für 1 Schritt (Jahr) in die Zukunft
forecast = model_fit.forecast(steps=1)

# Schön formatierte Ausgabe
print(f"Exponential Smoothing Forecast für das nächste Jahr ({forecast.index[0].year}): {forecast.iloc[0]:,.2f} $")
