import pandas as pd
from dtaidistance import dtw
import numpy as np

# 1. Read data
file_path = "Dis_world.txt"  # setting workpath
data = pd.read_csv(file_path, sep="\t")  

# 2. DTW analysis
metrics = ['VF', 'AMR score', 'AMR class', 'AMR gene']
dtw_results = {}

for metric in metrics:
  
    human_series = data[metric].values
    nonhuman_series = data[f"{metric}.1"].values

  
    distance = dtw.distance(human_series, nonhuman_series)


    dtw_results[metric] = distance

# 3. DTW distance output
for metric, distance in dtw_results.items():
    print(f"{metric} DTW ：{distance}")
