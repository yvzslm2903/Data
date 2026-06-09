import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_xlsx = pd.read_excel('/Users/yavuzselim/Desktop/Data Projekt/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx')
df_clean = df_xlsx.dropna()

etr = df_clean.groupby('State')['ETR'].mean().reset_index()
plt.rcParams["figure.figsize"] = (10,3)

sns.lineplot(data=etr, x = 'State', y = 'ETR', color='blue', marker='o',
            markersize = 8, markerfacecolor = 'black', markeredgecolor = 'black')

plt.xlabel("State", fontsize = 12)
plt.ylabel("ETR", fontsize = 12)

plt.tight_layout()
plt.show()
