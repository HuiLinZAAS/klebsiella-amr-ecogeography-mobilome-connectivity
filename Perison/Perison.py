import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Read data
file_path = "Dis_China.txt"  # setting workpath
data = pd.read_csv(file_path, sep="\t")  

# Selectting the corresponding metric for correlation analysis
metrics = ['VF', 'AMR score', 'AMR class', 'AMR gene']
correlation_results = {}

# The Pearson correlation coefficient for each pair of indicators is calculated
for metric in metrics:
    
    human_data = data[metric]
    nonhuman_data = data[f'{metric}.1']

   
    correlation = human_data.corr(nonhuman_data)
    correlation_results[metric] = correlation


for metric, correlation in correlation_results.items():
    print(f"{metric}: Pearson Correlation = {correlation:.4f}")


correlation_matrix = data[['VF', 'AMR score', 'AMR class', 'AMR gene',
                           'VF.1', 'AMR score.1', 'AMR class.1', 'AMR gene.1']].corr()

#heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for Human and Non-Human Corresponding Indicators')
plt.show()
