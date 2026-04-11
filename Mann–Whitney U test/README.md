Mann–Whitney U Test Analysis

Overview



This script performs Mann–Whitney U tests to compare differences between two independent groups (Human vs Nonhuman) across multiple AMR and VF-related metrics.



Input

Tab-separated text file (Dis\_China.txt)

Contains paired columns for Human and Nonhuman samples

Metrics analyzed

VF

AMR score

AMR class

AMR gene



Each metric has two columns:



Metric (Human)

Metric.1 (Nonhuman)

Method



For each metric, a Mann–Whitney U test is applied:



Non-parametric test for independent samples

Two-sided alternative hypothesis

Tests whether distributions differ between groups

Output



For each metric, the script reports:



U statistic

p-value

Interpretation

p < 0.05: significant difference between groups

p ≥ 0.05: no significant difference detected

Requirements

pandas

scipy

Usage



Run the script directly after setting the correct file path.

