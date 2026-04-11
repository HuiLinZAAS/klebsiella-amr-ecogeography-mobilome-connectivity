import pandas as pd
from scipy.stats import spearmanr

# 1. Read data
file_path = "Dis_world.txt"  # setting workpath
data = pd.read_csv(file_path, sep="\t")  

# 2. metrics setting
metrics = ['VF', 'AMR score', 'AMR class', 'AMR gene']
correlation_results = {}

# 3. Spearman analysis
for metric in metrics:
 
    human_data = data[metric]
    nonhuman_data = data[f'{metric}.1']

    
    rho, p_value = spearmanr(human_data, nonhuman_data)
    correlation_results[metric] = {'Spearman Correlation': rho, 'p-value': p_value}

# 4. result output
for metric, result in correlation_results.items():
    print(f"{metric}: Spearman Correlation = {result['Spearman Correlation']:.4f}, p-value = {result['p-value']:.4f}")
