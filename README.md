Eco-geography reverses dominant AMR reservoirs in Klebsiella pneumoniae
Overview

This project studies how AMR reservoirs in Klebsiella pneumoniae vary across ecology and geography using a One Health framework.

We analyze:

AMR burden
virulence
phylogeny
cross-niche patterns

Methods used:

Mann–Whitney U test
Pearson correlation
Spearman correlation
Permutation test
Variance partitioning
Bootstrap analysis
Files
human for resampling.xlsx: multi-database data
human for resampling/: plots output folder
Dis_China.txt: Human vs Nonhuman data (China)
Dis_world.txt: global Human vs Nonhuman data
SourceData_Permutation.csv: permutation input
Result_Permutaion.csv: permutation output
bootstrap_analysis.py: bootstrap analysis
permutation_test.R: permutation test script
Main analyses

Mann–Whitney U test: compare Human vs Nonhuman groups
Pearson correlation: linear relationship
Spearman correlation: rank-based relationship
Permutation test: randomization significance test
Variance partitioning: effect of ST, region, source
Bootstrap: resampling across databases

Model

AMR ~ Region + Source + (1 | ST)

Output
tables: statistical results
figures: boxplots, heatmaps
permutation distributions
bootstrap summaries
Requirements

pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl

R: tidyverse

Run

python bootstrap_analysis.py
python mann_whitney_u.py
python correlation_pearson.py
python correlation_spearman.py

R:
source("permutation_test.R")

Runtime

Bootstrap: < 5 min
Permutation: 5–15 min

License

For academic use only
