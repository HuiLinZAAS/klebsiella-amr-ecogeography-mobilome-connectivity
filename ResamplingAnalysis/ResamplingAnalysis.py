import os.path

import pandas as pd
import numpy as np
from scipy.stats import f_oneway, kruskal
from scikit_posthocs import posthoc_dunn
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load all worksheets from the data file
out_file = 'human for resampling' # non-human for resampling.xls
file_path = 'human for resampling.xlsx' #
sheets = pd.read_excel(file_path, sheet_name=None)  # Read all worksheets into a dictionary

# 2. Set sample sizes and number of bootstrap iterations
sample_sizes = [500, 1000, 1500] # Adjust as needed, e.g., [50,100,150] for non-human resampling
num_bootstraps = 1000

# 3. Prepare a dictionary to store bootstrap means for each database
bootstrap_means = {db: {size: {'AMRscore': [], 'AMRclass': [], 'AMRgene': [], 'VFscore': []} for size in sample_sizes}
                   for db in sheets.keys()}

# 4. Perform resampling and compute means
for db_name, db_data in sheets.items():
    for size in sample_sizes:
        for _ in range(num_bootstraps):
            # Resample data with replacement
            resample = db_data.sample(n=size, replace=False)
            # Compute the mean for each metric and store it in the dictionary
            bootstrap_means[db_name][size]['AMRscore'].append(resample['AMRscore'].mean())
            bootstrap_means[db_name][size]['AMRclass'].append(resample['AMRclass'].mean())
            bootstrap_means[db_name][size]['AMRgene'].append(resample['AMRgene'].mean())
            bootstrap_means[db_name][size]['VFscore'].append(resample['VFscore'].mean())

# 5. Convert results to DataFrame for comparison and visualization, and save means to CSV files
bootstrap_results = {}
for size in sample_sizes:
    result = pd.DataFrame({
        f"{db}_{metric}": bootstrap_means[db][size][metric]
        for db in bootstrap_means.keys()
        for metric in ['AMRscore', 'AMRclass', 'AMRgene', 'VFscore']
    })
    bootstrap_results[size] = result

    # Save means to a CSV file
    csv_file_name = f"non_human_bootstrap_means_{size}_samples.csv"
    result.to_csv(csv_file_name, index=False)
    print(f"Mean results saved to {csv_file_name}")

# 6. Define a function to perform various significance tests
def perform_statistical_tests(metric, sample_size_data, size):
    # Prepare data for testing
    values = []
    labels = []
    for db in bootstrap_means.keys():
        values.extend(sample_size_data[f"{db}_{metric}"].values)
        labels.extend([db] * num_bootstraps)

    # Perform ANOVA
    anova_result = f_oneway(*(sample_size_data[f"{db}_{metric}"] for db in bootstrap_means.keys()))
    significance_anova = "Significant" if anova_result.pvalue < 0.05 else "Not Significant"
    print(
        f"{metric} ANOVA results (Sample size {size}): F-statistic = {anova_result.statistic}, p-value = {anova_result.pvalue} -> {significance_anova}")

    # Perform Kruskal-Wallis test
    kruskal_result = kruskal(*(sample_size_data[f"{db}_{metric}"] for db in bootstrap_means.keys()))
    significance_kruskal = "Significant" if kruskal_result.pvalue < 0.05 else "Not Significant"
    print(
        f"{metric} Kruskal-Wallis results (Sample size {size}): H-statistic = {kruskal_result.statistic}, p-value = {kruskal_result.pvalue} -> {significance_kruskal}")

    # Perform Tukey HSD post-hoc test
    tukey_result = pairwise_tukeyhsd(values, labels)
    print(f"\n=== Tukey HSD significance comparison for {metric} at sample size {size} ===\n")
    print(tukey_result.summary())

    # Perform Dunn's test (post-hoc test for Kruskal-Wallis) and convert to significance boolean matrix
    dunn_result = posthoc_dunn([sample_size_data[f"{db}_{metric}"] for db in bootstrap_means.keys()],
                               p_adjust='bonferroni')
    dunn_significance = dunn_result < 0.05  # Convert to significance boolean matrix
    print(f"\n=== Dunn's significance boolean matrix for {metric} at sample size {size} ===\n")
    print(dunn_significance)

    return anova_result, kruskal_result, tukey_result, dunn_significance

# 7. Analysis and visualization
metrics = ['AMRscore', 'AMRclass', 'AMRgene', 'VFscore']

for size in sample_sizes:
    sample_size_data = bootstrap_results[size]
    print(f"\n=== Analysis results for sample size {size} ===\n")
    for metric in metrics:
        # Perform various significance tests
        anova_result, kruskal_result, tukey_result, dunn_significance = perform_statistical_tests(metric,
                                                                                                  sample_size_data,
                                                                                                  size)

        # Prepare data for visualization
        metric_data = sample_size_data.filter(regex=metric)
        metric_long = pd.melt(metric_data, var_name="Database", value_name=metric)
        metric_long["Database"] = metric_long["Database"].str.replace(f"_{metric}", "")

        # Create a box plot, set large font sizes and palette, and save the image
        plt.figure(figsize=(12, 8))
        sns.boxplot(x="Database", y=metric, data=metric_long, hue="Database", palette="Set2", legend=False)

        # sns.boxplot(x="Database", y=metric, data=metric_long, palette="Set2")
        plt.title(f"{metric} Comparisons Between Databases at {size} Sample Size", fontsize=16)
        plt.ylabel(metric, fontsize=14)
        plt.xlabel("Database", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        # Save the image
        file_name = f"human-{metric}_Comparisons_{size}_SampleSize.png"
        out_path=os.path.join(out_file, file_name)
        plt.savefig(out_path)
        plt.show()
