Pearson Correlation Analysis

Overview



This script calculates Pearson correlation coefficients between paired Human and Nonhuman groups across multiple AMR and VF-related metrics, and visualizes the correlation structure using a heatmap.



Input

Tab-separated file: Dis\_China.txt

Contains paired columns for Human and Nonhuman samples

Metrics analyzed

VF

AMR score

AMR class

AMR gene



Each metric has two columns:



Metric (Human)

Metric.1 (Nonhuman)

Methods

1\. Pairwise Pearson correlation



For each metric:



Compute Pearson correlation between Human and Nonhuman values

2\. Global correlation matrix

Calculate correlation matrix across all variables:

Human metrics

Nonhuman metrics

Output

Console output

Pearson correlation coefficient for each metric pair

Visualization

Heatmap of full correlation matrix

Interpretation

r > 0.7: strong positive correlation

0.3 < r < 0.7: moderate correlation

r < 0.3: weak correlation

Requirements

pandas

seaborn

matplotlib

Usage



Run the script after setting the correct file path.

