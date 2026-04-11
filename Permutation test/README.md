Permutation Test Analysis

Overview



This script performs a permutation test to evaluate whether species–group associations are significantly different from random expectation.



Input

File: SourceData\_Permutation.csv

Columns:

species\_abbv

group\_summary

Method

1\. Observed structure

Count occurrences of each species × group combination

2\. Permutation procedure

Randomly shuffle group\_summary labels

Repeat 10,000 permutations

Recalculate species–group counts for each permutation

3\. Null distribution

Generate empirical distribution of counts under random assignment

Statistical test



For each species–group pair:



Compare observed count vs permutation distribution

Calculate empirical p-values:

Over-representation (greater than expected)

Under-representation (less than expected)

Multiple testing correction

Benjamini–Hochberg (BH) correction applied

Significant threshold: adjusted p < 0.025

Output

File



Result\_Permutaion.csv



Contents

Observed counts

Permutation-based p-values

Adjusted p-values (BH correction)

Enrichment direction:

over-represented

under-represented

non-significant

Visualization

Histogram of permutation counts

Observed counts marked with dashed red line

Faceted by species and group

Interpretation

Significant “over” → species enriched in a group

Significant “under” → species depleted in a group

Non-significant → random expectation

Requirements

tidyverse (dplyr, ggplot2, tidyr, readr)

Usage



Run the script after setting working directory and input file path.

