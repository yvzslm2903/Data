import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_xlsx = pd.read_excel('/Users/yavuzselim/Desktop/Data Projekt/Analytics_mindset_case_study_solutions_Trinas_Trinkets.xlsx')
df_clean = df_xlsx.dropna()
df_clean.info()

profit_staat = df_clean.groupby('State')['Profit'].sum().reset_index()
plt.rcParams["figure.figsize"] = (10,3)

sns.barplot(data=profit_staat, x='State', y='Profit', palette='magma', edgecolor='black')
#Lineplot eigenschaften sind -> palette='magma', edgecolor='black'
#In diesem Fall macht ein Barplot mehr sinn 
plt.xlabel("State", fontsize=12)
plt.ylabel("Profit", fontsize=12)

plt.tight_layout()
plt.show()



