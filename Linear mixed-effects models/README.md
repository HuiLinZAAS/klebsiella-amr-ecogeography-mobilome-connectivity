AMR–Phylogeny Variance Partition Analysis
Overview

This project analyzes whether antimicrobial resistance (AMR) variation in Klebsiella pneumoniae is mainly driven by phylogeny (sequence type, ST), geographic region, or host source.

Input data
Global K. pneumoniae genome dataset (Excel file)
Country-to-region classification file
AMR traits
Resistance_score
Resistance_genes
Resistance_classes
Virulence_score
Method

For each AMR trait, two models are fitted:

Mixed-effects model (with phylogeny):

AMR ~ Region2 + Source + (1 | ST)

Linear model (without phylogeny):

AMR ~ Region2 + Source

Phylogenetic contribution is estimated as:

Var(ST) / (Var(ST) + Residual variance)

Model comparison is based on:

variance partitioning
R² of fixed effects
log-likelihood difference
Output
Excel file with summary statistics and model coefficients
Boxplot figures showing AMR distribution across region and source
Requirements
R packages: readxl, dplyr, lme4, lmerTest, broom, openxlsx, ggplot2
Usage

Run the R script after setting working directory and input file paths.
