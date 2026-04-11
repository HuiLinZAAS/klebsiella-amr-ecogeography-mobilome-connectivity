Spearman Correlation Analysis

Overview



This script calculates Spearman rank correlation between paired Human and Nonhuman groups across multiple AMR and VF-related metrics.



Input

Tab-separated file: Dis\_world.txt

Contains paired columns for Human and Nonhuman samples

Metrics analyzed

VF

AMR score

AMR class

AMR gene



Each metric includes two columns:



Metric (Human)

Metric.1 (Nonhuman)

Method



For each metric:



Compute Spearman rank correlation (ρ)

Test monotonic relationship between Human and Nonhuman values

Non-parametric approach (based on ranks)

Output



For each metric, the script reports:



Spearman correlation coefficient (ρ)

p-value

Interpretation

ρ > 0.7: strong positive monotonic relationship

0.3 < ρ < 0.7: moderate relationship

ρ < 0.3: weak relationship

p < 0.05: statistically significant correlation

Requirements

pandas

scipy

Usage



Run the script after setting the correct file path.

