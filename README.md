Eco-geography reverses dominant AMR reservoirs in Klebsiella pneumoniae
Overview

This project investigates how antimicrobial resistance (AMR) reservoirs in Klebsiella pneumoniae vary across ecological and geographic contexts using a One Health framework.

We integrate large-scale genomic and metadata datasets to quantify:

AMR burden
virulence features
phylogenetic structure
cross-niche connectivity

Statistical analyses include:

Mann–Whitney U test
Pearson correlation
Spearman correlation
Permutation test
Variance partitioning (mixed models)
Bootstrap analysis
Project Structure
├── human for resampling.xlsx
├── human for resampling/
├── human-*.png
├── human_bootstrap_means_*.csv
├── Dis_China.txt
├── Dis_world.txt
├── SourceData_Permutation.csv
├── AMR_phylogeny_variance_partition.xlsx
├── Result_Permutaion.csv
├── bootstrap_analysis.py
├── correlation_pearson.py
├── correlation_spearman.py
├── mann_whitney_u.py
├── permutation_test.R
└── README.md
Statistical Analyses
Mann–Whitney U Test

Non-parametric test comparing Human vs Nonhuman groups.

Pearson Correlation

Measures linear correlation between paired variables.

Spearman Correlation

Rank-based correlation for monotonic relationships.

Permutation Test
10,000 permutations
Empirical p-values
BH correction
Variance Partitioning
AMR ~ Region + Source + (1 | ST)

Estimates:

phylogenetic effect (ST)
ecological effects (region/source)
Bootstrap Analysis
Sample sizes: 500 / 1000 / 1500
1000 iterations each
Statistical tests:
ANOVA
Kruskal–Wallis
Tukey HSD
Dunn test (Bonferroni)
Input Data
AMRscore
AMRclass
AMRgene
VFscore
Outputs
Tables
bootstrap results
permutation results
correlation results
variance partitioning results
Figures
boxplots
heatmaps
permutation histograms
Requirements
pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl

R:

tidyverse
Usage

Python:

python bootstrap_analysis.py
python mann_whitney_u.py
python correlation_pearson.py
python correlation_spearman.py

R:

source("permutation_test.R")
Runtime
Bootstrap: < 5 minutes
Permutation test: 5–15 minutes
License

For academic use only.
