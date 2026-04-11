Eco-geography reverses dominant AMR reservoirs in Klebsiella pneumoniae
Overview

This project investigates how antimicrobial resistance (AMR) reservoirs in Klebsiella pneumoniae vary across ecological and geographic contexts using a One Health framework.

We integrate large-scale genomic and metadata datasets to quantify:

AMR burden
virulence features
phylogenetic structure
cross-niche connectivity

Multiple statistical approaches are used, including:

non-parametric tests (Mann–Whitney U)
correlation analyses (Pearson, Spearman)
permutation tests
variance partitioning with mixed models
bootstrap resampling
Project Structure
├── human for resampling.xlsx              # Multi-sheet Excel (different databases)
├── human for resampling/                 # Output plots folder
├── human-*.png                          # Boxplots
├── human_bootstrap_means_*.csv         # Bootstrap results
├── Dis_China.txt                       # Human vs Nonhuman paired data (China)
├── Dis_world.txt                       # Human vs Nonhuman paired data (global)
├── SourceData_Permutation.csv         # Permutation test input
├── AMR_phylogeny_variance_partition.xlsx
├── Result_Permutaion.csv
├── bootstrap_analysis.py              # Main bootstrap script
├── correlation_pearson.py            # Pearson analysis
├── correlation_spearman.py           # Spearman analysis
├── mann_whitney_u.py                 # Mann–Whitney U test
├── permutation_test.R                # Permutation analysis (R)
└── README.md
Statistical Analyses
1. Mann–Whitney U Test

Non-parametric test comparing Human vs Nonhuman groups.

Tests differences in distributions
Used for:
VF
AMR score
AMR class
AMR gene
2. Pearson Correlation

Measures linear relationships between paired variables.

Human vs Nonhuman comparisons
Correlation matrix visualization (heatmap)
3. Spearman Correlation

Non-parametric rank-based correlation.

Measures monotonic relationships
Robust to outliers and non-normality
4. Permutation Test

Evaluates whether species–group associations deviate from randomness.

10,000 permutations
Empirical p-values
Benjamini–Hochberg correction
5. Variance Partitioning (Mixed Models)

Model:

AMR ~ Region + Source + (1 | ST)

Quantifies:

contribution of phylogeny (ST)
environmental effects (region/source)
6. Bootstrap Analysis

Input: multi-database Excel file

Procedure:

Resampling at sizes: 500 / 1000 / 1500
1000 iterations each
Compute mean AMR/VF metrics

Statistical tests:

ANOVA
Kruskal–Wallis
Tukey HSD
Dunn’s test (Bonferroni corrected)
Key Input Data Columns

Each dataset includes:

AMRscore
AMRclass
AMRgene
VFscore
Outputs
Tables
Bootstrap mean results
Permutation p-values
Mixed model variance partitioning
Correlation coefficients
Figures
Boxplots across databases
Correlation heatmaps
Permutation distributions
Requirements
pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl

R dependencies (for permutation test):

tidyverse
Usage
Python analyses
python bootstrap_analysis.py
python mann_whitney_u.py
python correlation_pearson.py
python correlation_spearman.py
R permutation test
source("permutation_test.R")
Runtime
Bootstrap (1000 iterations × 3 sample sizes): < 5 minutes
Permutation test (10,000 reps): ~5–15 minutes depending on CPU
Key Interpretation
High phylogenetic variance → lineage-driven AMR structure
High ecological effect → environment-driven AMR distribution
Significant permutation results → non-random species–group association
Correlation consistency → robustness across methods
License

Academic and research use only.
