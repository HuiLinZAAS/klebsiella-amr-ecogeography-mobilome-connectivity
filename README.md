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


## Project Modules

This project is organized into multiple analytical modules:

### 1. Klebsiella pneumoniae global genome workflow
Klebsiella-pneumoniae-global-genome-workflow  
Global dataset processing and One Health integration of *Klebsiella pneumoniae* genomes.

---

### 2. Linear mixed-effects models
Linear mixed-effects models  
Variance partitioning framework using mixed models:

AMR ~ Region + Source + (1 | ST)

Used to quantify phylogenetic vs ecological contributions.

---

### 3. Mann–Whitney U test
Mann–Whitney U test  
Non-parametric comparison between Human and Nonhuman groups.

---

### 4. Pearson correlation
Pearson correlation  
Measures linear relationships between paired AMR/VF variables.

---

### 5. Spearman correlation
Spearman correlation  
Rank-based correlation for monotonic relationships and non-normal data.

---

### 6. Permutation test
Permutation test  
Randomization-based test (10,000 permutations) to assess significance of species–group associations.

---

### 7. Plasmid replicon similarity network
Plasmid replicon similarity network  
Network-based analysis of plasmid replicon sharing across genomes to evaluate horizontal gene transfer and connectivity.

---

### 8. Sharing event analysis
SharingEvent  
Analysis of cross-niche or cross-source sharing events in AMR and mobilome data.

---

### 9. Resampling analysis
ResamplingAnalysis  
Bootstrap-based framework for estimating robustness of AMR/VF patterns across different sample sizes (500 / 1000 / 1500).

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

pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl
install.packages("tidyverse")
python bootstrap_analysis.py
python mann_whitney_u.py
python correlation_pearson.py
python correlation_spearman.py
source("permutation_test.R")

#License

This project is for academic and research use only.
