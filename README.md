# Bootstrap Resampling and Statistical Comparison of Human Datasets

This project performs bootstrap resampling of human dataset sheets, calculates the means of key indicators (e.g., AMRscore, AMRclass, AMRgene, VFscore), and conducts statistical comparisons including ANOVA, Kruskal-Wallis, Tukey HSD, and Dunn's tests. It also generates boxplots to visualize differences between databases across different sample sizes.

## Project Structure

```
├── human for resampling.xlsx           # Excel file with multiple sheets representing different databases
├── human for resampling/              # Folder where result plots will be saved
├── human-*.png                        # Boxplot outputs
├── human_bootstrap_means_*.csv       # CSV files storing bootstrap mean results
├── README.md                          # This file
└── bootstrap_analysis.py              # Main Python script
```

## Requirements

Install dependencies via pip:

```bash
pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl
```

## How to Use

1. **Place your Excel file** named `human for resampling.xlsx` in the root directory. Each worksheet should represent a different database, and each sheet must contain columns:
   - `AMRscore`
   - `AMRclass`
   - `AMRgene`
   - `VFscore`

2. **Run the script:**

```bash
python bootstrap_analysis.py
```

This will:
- Perform bootstrap resampling for sample sizes of 500, 1000, and 1500 (with 1000 iterations each).
- Calculate the mean values for each metric per database.
- Conduct statistical tests:
  - ANOVA
  - Kruskal-Wallis
  - Tukey's HSD
  - Dunn’s post-hoc test (with Bonferroni correction)
- Save statistical results to the console and export visualizations as `.png` files and data as `.csv`.

## Output

- `human_bootstrap_means_<sample_size>_samples.csv`: Bootstrap mean results for each sample size.
- `human-<metric>_Comparisons_<sample_size>_SampleSize.png`: Boxplots showing the distribution of bootstrap means across databases.
- Console output includes test statistics and post-hoc test significance summaries.

## Notes

- This project assumes that sampling is done without replacement.
- For non-human data, modify the input Excel filename and output folder name in the script accordingly.

---

## System Requirements and Runtime Estimates

### Environment

- **Recommended Operating Systems**:
  - Windows 10/11
  - macOS 11 or later
  - Ubuntu 20.04 or later
- **Tested Python Version**:
  - Python 3.10.12

Check your Python version with:

```bash
python --version
```

### Setup Time

- Installing required packages typically takes **1–3 minutes**:

```bash
pip install pandas numpy scipy matplotlib seaborn statsmodels scikit-posthocs openpyxl
```

### Runtime Estimates

- On a typical modern machine using Python 3.10.12:
  - Full bootstrap analysis with 1000 iterations for each sample size (500, 1000, 1500) completes in **under 5 minutes** total.
  - Performance may vary slightly with CPU speed and number of Excel sheets.

You can measure runtime using:

```bash
time python bootstrap_analysis.py
```

---

## License

This project is for academic and research use only.
