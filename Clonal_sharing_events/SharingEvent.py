import pandas as pd
import numpy as np
import random
import os
from scipy.stats import ttest_ind, mannwhitneyu

def count_transmission_events(matrix, threshold=10, verberose=False):
    """Count the number of transmission events with SNP distance ≤ threshold."""
    # Only calculate the lower triangle of the matrix to avoid duplication (symmetric matrix)
    mask = np.tril(matrix.values, k=-1)  # k=-1 excludes the diagonal
    event_mask = (mask <= threshold) & (mask > 0)  # exclude cases where distance = 0

    if verberose:
        event_indices_np = np.where(event_mask)
        event_indices = list(zip(event_indices_np[0], event_indices_np[1]))
        for i, j in event_indices:
            print(f'SNP distance between {matrix.index[i]} and {matrix.columns[j]} is less than or equal to {threshold}')
    return np.sum(event_mask)


def random_sampling_transmission_events(matrix, sample_list, sample_size=94, num_iterations=1000, threshold=10):
    """Randomly sample from the given strain list and calculate average number of transmission events (SNP ≤ threshold)."""
    transmission_counts = []

    for _ in range(num_iterations):
        # Randomly sample strains from the list
        sampled_bacteria = random.sample(sample_list, sample_size)

        # Extract submatrix from the full distance matrix
        sampled_matrix = matrix.loc[sampled_bacteria, sampled_bacteria]

        # Count number of transmission events
        transmission_count = count_transmission_events(sampled_matrix, threshold=threshold)
        transmission_counts.append(transmission_count)

    return {
        'average': np.mean(transmission_counts),
        'max': np.max(transmission_counts),
        'min': np.min(transmission_counts),
        'median': np.median(transmission_counts),
        'all_counts': transmission_counts
    }


def calcaulating_transmission_events(matrix, sample_list):
    sampled_matrix = matrix.loc[sample_list, sample_list]
    transmission_count = count_transmission_events(sampled_matrix, threshold=10)
    return transmission_count


def load_sample_list(data_path, distance_df):
    bacteria_list_df = pd.read_excel(data_path)
    bacteria_list = bacteria_list_df.iloc[:, 0].tolist()  # Convert to strain name list
    bacteria_list_true = [b for b in bacteria_list if b in distance_df.index]
    if len(bacteria_list_true) < len(bacteria_list):
        removed = set(bacteria_list) - set(bacteria_list_true)
        for b in removed:
            print(f"Strain {b} not found in the distance matrix and has been removed.")
    return bacteria_list_true


def compare_transmission_events(hospital_counts, community_counts):
    """Compare whether transmission events differ significantly between community and hospital."""
    t_stat, t_p_value = ttest_ind(hospital_counts, community_counts, equal_var=False)
    u_stat, u_p_value = mannwhitneyu(hospital_counts, community_counts, alternative='two-sided')

    print("T-test result:")
    print(f"T-statistic: {t_stat}, p-value: {t_p_value}, Significant: {'Yes' if t_p_value < 0.05 else 'No'}")
    print("Mann-Whitney U test result:")
    print(f"U-statistic: {u_stat}, p-value: {u_p_value}, Significant: {'Yes' if u_p_value < 0.05 else 'No'}")


# Read Excel file, use first row as column names and first column as index
df = pd.read_excel('snp-dis.xlsx', index_col=0)
# Clean row and column names
df.index = df.index.str.replace(r'^JAX[A-Z0-9]*_', '', regex=True)
df.columns = df.columns.str.replace(r'^JAX[A-Z0-9]*_', '', regex=True)

# Load strain list
community_data_path = 'Community_sample_list.xlsx'
hospital_data_path = 'Hospital_sample_list.xlsx'

hospital_samples_list = load_sample_list(hospital_data_path, df)
community_samples_list = load_sample_list(community_data_path, df)

output_dir = "output_results_ttt"
os.makedirs(output_dir, exist_ok=True)

for sample_size in [50, 60, 70, 80]:
    for num_iterations in [100, 1000, 10000]:
        hospital_results = random_sampling_transmission_events(
            df, hospital_samples_list, sample_size=sample_size, num_iterations=num_iterations)
        community_results = random_sampling_transmission_events(
            df, community_samples_list, sample_size=sample_size, num_iterations=num_iterations)

        # Print result summary
        print(f"========== Results ==========")
        print(f"Sample size: {sample_size}, Resampling iterations: {num_iterations}")
        print(f"Hospital avg. transmission events: {hospital_results['average']}")
        print(f"Community avg. transmission events: {community_results['average']}")

        # Save summary statistics
        hospital_summary_filename = f"Hospital_stats_{sample_size}_{num_iterations}.csv"
        community_summary_filename = f"Community_stats_{sample_size}_{num_iterations}.csv"
        hospital_summary_filepath = os.path.join(output_dir, hospital_summary_filename)
        community_summary_filepath = os.path.join(output_dir, community_summary_filename)

        hospital_summary_data = {
            'Average Transmission Events': [hospital_results['average']],
            'Max Transmission Events': [hospital_results['max']],
            'Min Transmission Events': [hospital_results['min']],
            'Median Transmission Events': [hospital_results['median']]
        }
        community_summary_data = {
            'Average Transmission Events': [community_results['average']],
            'Max Transmission Events': [community_results['max']],
            'Min Transmission Events': [community_results['min']],
            'Median Transmission Events': [community_results['median']]
        }

        hospital_summary_df = pd.DataFrame(hospital_summary_data)
        community_summary_df = pd.DataFrame(community_summary_data)

        hospital_summary_df.to_csv(hospital_summary_filepath, index=False)
        community_summary_df.to_csv(community_summary_filepath, index=False)

        # Save all transmission event counts
        hospital_counts_filename = f"Hospital_transmission_counts_{sample_size}_{num_iterations}.csv"
        community_counts_filename = f"Community_transmission_counts_{sample_size}_{num_iterations}.csv"
        hospital_counts_filepath = os.path.join(output_dir, hospital_counts_filename)
        community_counts_filepath = os.path.join(output_dir, community_counts_filename)

        hospital_result_df = pd.DataFrame({'Transmission Counts': hospital_results['all_counts']})
        community_result_df = pd.DataFrame({'Transmission Counts': community_results['all_counts']})

        hospital_result_df.to_csv(hospital_counts_filepath, index=False)
        community_result_df.to_csv(community_counts_filepath, index=False)

        # Perform significance test
        compare_transmission_events(hospital_results['all_counts'], community_results['all_counts'])
