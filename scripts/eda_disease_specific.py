# scripts/eda_disease_specific.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from pathlib import Path

# Load cleaned summary (country-year level)
summary = pd.read_csv("outputs/eda_cleaned_summary.csv")

# Diseases of interest (we’ll analyze trends using total_cases and avg_incidence_per_100k)
diseases_of_interest = ["MEASLES", "POLIO", "HEPATITIS B", "DTP", "INFLUENZA"]

# If your cleaned summary has no disease column, you may need to merge with incidence or reported_cases table
# For now, let's assume we only have overall coverage vs incidence/cases

out_dir = Path("outputs/disease_specific")
out_dir.mkdir(exist_ok=True)

results = []

for disease in diseases_of_interest:
    # Filter the original incidence/coverage data if needed (for this example we work with summary only)
    df = summary.copy()  # Replace with filtered disease data if merged from incidence table
    
    # Skip empty dataframes
    if df.empty:
        continue

    # Correlations
    pearson_cov_inc = pearsonr(df["avg_coverage"], df["avg_incidence_per_100k"])
    spearman_cov_inc = spearmanr(df["avg_coverage"], df["avg_incidence_per_100k"])

    pearson_cov_cases = pearsonr(df["avg_coverage"], df["total_cases"])
    spearman_cov_cases = spearmanr(df["avg_coverage"], df["total_cases"])

    results.append({
        "disease": disease,
        "n": len(df),
        "pearson_cov_inc": pearson_cov_inc[0],
        "spearman_cov_inc": spearman_cov_inc.correlation,
        "pearson_cov_cases": pearson_cov_cases[0],
        "spearman_cov_cases": spearman_cov_cases.correlation,
    })

    # Line plot: coverage vs incidence over time
    plt.figure(figsize=(10,6))
    sns.lineplot(data=df, x="year", y="avg_coverage", label="Coverage", color="blue")
    sns.lineplot(data=df, x="year", y="avg_incidence_per_100k", label="Incidence/100k", color="red")
    plt.title(f"{disease}: Coverage vs Incidence over time")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / f"{disease}_trend.png")
    plt.close()

# Save summary table
pd.DataFrame(results).to_csv(out_dir / "disease_specific_summary.csv", index=False)

print("Disease-specific EDA complete. Results in outputs/disease_specific/")
