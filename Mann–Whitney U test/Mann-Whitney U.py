import pandas as pd
from scipy.stats import mannwhitneyu

# 1. Read the data
file_path = 'Dis_China.txt'  # working path
data = pd.read_csv(file_path, sep="\t")  

# 2. Rename columns
data.columns = ['Year', 'VF', 'AMR score', 'AMR class', 'AMR gene',
                'VF.1', 'AMR score.1', 'AMR class.1', 'AMR gene.1']

# 3. Metrics list
metrics = ['VF', 'AMR score', 'AMR class', 'AMR gene']

# 4. Mann-Whitney U Test
results = {}
for metric in metrics:
    
    human_data = data[metric]
    nonhuman_data = data[f'{metric}.1']

    
    u_stat, p_value = mannwhitneyu(human_data, nonhuman_data, alternative='two-sided')
    results[metric] = {'U statistic': u_stat, 'p-value': p_value}

# 5. Result output
print("\nMann-Whitney U：")
for metric, result in results.items():
    print(f"{metric}: U = {result['U statistic']:.2f}, p = {result['p-value']:.4f}")
