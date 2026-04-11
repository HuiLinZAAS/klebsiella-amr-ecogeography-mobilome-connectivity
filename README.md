# Eco-geography reverses dominant AMR reservoirs in *Klebsiella pneumoniae*

## Overview

This project investigates how antimicrobial resistance (AMR) reservoirs in *Klebsiella pneumoniae* vary across ecological and geographic contexts using a One Health framework.

We integrate large-scale genomic and metadata datasets to quantify:

- AMR burden  
- virulence features  
- phylogenetic structure  
- cross-niche connectivity  

Multiple statistical approaches are used:

- Mann–Whitney U test  
- Pearson correlation  
- Spearman correlation  
- Permutation test  
- Variance partitioning (mixed models)  
- Bootstrap analysis  

---

## Project Structure


---

## Statistical Analyses

### 1. Mann–Whitney U Test
Non-parametric test comparing Human vs Nonhuman groups.

Used for:
- VF
- AMR score
- AMR class
- AMR gene

---

### 2. Pearson Correlation
Measures linear relationships between paired variables.

- Human vs Nonhuman comparison  
- Correlation matrix (heatmap)

---

### 3. Spearman Correlation
Rank-based non-parametric correlation.

- Measures monotonic relationships  
- Robust to outliers

---

### 4. Permutation Test
Evaluates whether species–group associations deviate from randomness.

- 10,000 permutations  
- Empirical p-values  
- BH correction

---

### 5. Variance Partitioning

Model:

Estimates:
- phylogenetic contribution (ST)
- ecological effects (region/source)

---

### 6. Bootstrap Analysis

Input: multi-database Excel file

Procedure:
- Sample sizes: 500 / 1000 / 1500  
- 1000 iterations per size  
- Compute mean AMR/VF metrics  

Statistical tests:
- ANOVA  
- Kruskal–Wallis  
- Tukey HSD  
- Dunn’s test (Bonferroni)

---

## Input Data Columns

- AMRscore  
- AMRclass  
- AMRgene  
- VFscore  

---

## Outputs

### Tables
- Bootstrap results  
- Permutation p-values  
- Correlations  
- Variance partition results  

### Figures
- Boxplots  
- Heatmaps  
- Permutation histograms  

---

## Requirements

```bash
pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl
