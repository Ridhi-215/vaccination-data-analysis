# scripts/eda.py
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---- paths ----
proc_dir = "data/processed"
out_dir = "outputs/eda_plots"
os.makedirs(out_dir, exist_ok=True)

# ---- load cleaned CSVs ----
coverage = pd.read_csv(os.path.join(proc_dir, "coverage.csv"))
incidence = pd.read_csv(os.path.join(proc_dir, "incidence.csv"))
reported = pd.read_csv(os.path.join(proc_dir, "reported_cases.csv"))
intro = pd.read_csv(os.path.join(proc_dir, "vaccine_introduction.csv"))
schedule = pd.read_csv(os.path.join(proc_dir, "vaccine_schedule.csv"))

# Standardize column names to lowercase for safety
for df in [coverage, incidence, reported, intro, schedule]:
    df.columns = [c.lower() for c in df.columns]

# ---- helper: quick summary ----
def summarise_df(df, name):
    print(f"\n=== {name} ===")
    print("shape:", df.shape)
    print("dtypes:\n", df.dtypes)
    print("\nmissing values (top 20):\n", df.isna().sum().sort_values(ascending=False).head(20))
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        print("\nNumeric describe:\n", numeric.describe().T)
    print("-" * 40)

# Summaries
summarise_df(coverage, "coverage")
summarise_df(incidence, "incidence")
summarise_df(reported, "reported_cases")

# ---- Basic stats and distribution plots ----
def hist_plot(series, title, fname, bins=30):
    plt.figure(figsize=(7,4))
    sns.histplot(series.dropna(), bins=bins, kde=True)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, fname))
    plt.close()

# Coverage distribution
hist_plot(coverage['coverage'], "Distribution of coverage (%)", "hist_coverage.png")

# Incidence distribution
if 'incidence_rate' in incidence.columns:
    hist_plot(incidence['incidence_rate'], "Distribution of incidence_rate", "hist_incidence_rate.png")

# Reported cases distribution
if 'cases' in reported.columns:
    hist_plot(reported['cases'], "Distribution of reported cases", "hist_reported_cases.png")

# ---- Aggregations: country-year level ----
cov_agg = coverage.groupby(['code','year'], as_index=False).agg(
    avg_coverage = ('coverage','mean'),
    median_coverage = ('coverage','median'),
    doses_sum = ('doses','sum'),
    target_sum = ('target_number','sum'),
    coverage_count = ('coverage','count')
)

inc_agg = incidence.groupby(['code','year'], as_index=False).agg(
    avg_incidence_rate = ('incidence_rate','mean'),
    incidence_count = ('incidence_rate','count')
)

rep_agg = reported.groupby(['code','year'], as_index=False).agg(
    total_cases = ('cases','sum')
)

# Merge them
merged = cov_agg.merge(inc_agg, on=['code','year'], how='outer').merge(rep_agg, on=['code','year'], how='outer')

# Save aggregated CSV
os.makedirs("outputs", exist_ok=True)
merged.to_csv("outputs/eda_summary.csv", index=False)

# ---- Correlation analysis ----
corr_pairs = []
def compute_corr(x, y, name_x, name_y):
    df = merged[[x,y]].dropna()
    if len(df) < 5:
        return None
    pear = df[x].corr(df[y], method='pearson')
    spear = df[x].corr(df[y], method='spearman')
    corr_pairs.append((name_x, name_y, pear, spear, len(df)))
    return pear, spear

compute_corr('avg_coverage','avg_incidence_rate','avg_coverage','avg_incidence_rate')
compute_corr('avg_coverage','total_cases','avg_coverage','total_cases')

# Print correlation summary
print("\nCorrelation summary (country-year):")
for rec in corr_pairs:
    print(f"{rec[0]} vs {rec[1]}: Pearson={rec[2]:.4f}  Spearman={rec[3]:.4f}  n={rec[4]}")

# ---- Scatter plots with correlation annotation ----
def scatter_with_corr(xcol, ycol, df, title, fname):
    df2 = df[[xcol,ycol,'code','year']].dropna()
    if df2.empty:
        print("No data for", title)
        return
    pear = df2[xcol].corr(df2[ycol], method='pearson')
    plt.figure(figsize=(7,6))
    sns.scatterplot(data=df2, x=xcol, y=ycol, alpha=0.6)
    plt.title(f"{title}\nPearson r = {pear:.3f}")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, fname))
    plt.close()

scatter_with_corr('avg_coverage','avg_incidence_rate', merged, "Avg coverage vs Avg incidence rate", "scatter_cov_inc.png")
scatter_with_corr('avg_coverage','total_cases', merged, "Avg coverage vs Total reported cases", "scatter_cov_cases.png")

# ---- Correlation heatmap of numeric aggregated columns ----
num_cols = ['avg_coverage','median_coverage','doses_sum','target_sum','avg_incidence_rate','total_cases']
corr_df = merged[num_cols].corr()
plt.figure(figsize=(9,7))
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap='coolwarm', center=0)
plt.title("Correlation matrix (aggregated country-year)")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "heatmap_corr.png"))
plt.close()

# ---- Time series: global average coverage by year ----
if 'year' in coverage.columns:
    ts = coverage.groupby('year', as_index=False)['coverage'].mean().sort_values('year')
    plt.figure(figsize=(8,4))
    sns.lineplot(data=ts, x='year', y='coverage', marker='o')
    plt.title("Global average coverage by year")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "ts_global_avg_coverage.png"))
    plt.close()

# ---- Top/Bottom countries by mean coverage ----
country_cov = coverage.groupby('code', as_index=False).agg(mean_cov=('coverage','mean')).sort_values('mean_cov')
top10_low = country_cov.head(10)
top10_high = country_cov.tail(10)

plt.figure(figsize=(8,4))
sns.barplot(data=top10_low, x='mean_cov', y='code')
plt.title("Top 10 countries with lowest mean coverage")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "top10_low_coverage.png"))
plt.close()

plt.figure(figsize=(8,4))
sns.barplot(data=top10_high, x='mean_cov', y='code')
plt.title("Top 10 countries with highest mean coverage")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "top10_high_coverage.png"))
plt.close()

# ---- Drop-off between dose 1 and subsequent doses (best-effort) ----
# We attempt to extract trailing digits from antigen (e.g., POL1, POL2, POL3 or DIPHCV4)
def split_antigen_code(code):
    if pd.isna(code):
        return None, None
    m = re.match(r"^(.+?)(\d+)$", str(code))
    if m:
        base = m.group(1)
        dose = int(m.group(2))
        return base, dose
    return None, None

cov = coverage.copy()
cov[['antigen_base','antigen_dose']] = cov['antigen'].astype(str).apply(lambda x: pd.Series(split_antigen_code(x)))

# Keep only those with dose info
cov_dose = cov.dropna(subset=['antigen_base','antigen_dose'])
if not cov_dose.empty:
    # pivot so dose numbers are columns
    pivot = cov_dose.pivot_table(index=['code','year','antigen_base'], columns='antigen_dose', values='coverage', aggfunc='mean')
    # compute drop from dose1 to max dose
    def compute_drop(row):
        doses = sorted([c for c in row.index if not pd.isna(row[c])])
        if not doses:
            return np.nan
        first = row.get(1, np.nan)
        last = row[doses[-1]]
        if pd.isna(first) or pd.isna(last) or first == 0:
            return np.nan
        return (first - last) / first
    pivot['drop_pct'] = pivot.apply(compute_drop, axis=1)
    drop_summary = pivot['drop_pct'].dropna().reset_index()
    if not drop_summary.empty:
        drop_summary.to_csv("outputs/dose_drop_summary.csv", index=False)
        # simple histogram of drop %
        plt.figure(figsize=(7,4))
        sns.histplot(drop_summary['drop_pct']*100, bins=30, kde=True)
        plt.title("Distribution of drop (%) from dose1 to last dose (where identifiable)")
        plt.xlabel("Drop (%)")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "drop_from_dose1.png"))
        plt.close()
    else:
        print("No usable dose-based drop data found.")
else:
    print("No antigen codes with trailing dose numbers found (cannot compute dose drop-offs).")

# ---- Final notes and saved outputs ----
print("\nEDA complete. Plots and summaries saved to:", out_dir)
print("Aggregated country-year summary saved to: outputs/eda_summary.csv")
if os.path.exists("outputs/dose_drop_summary.csv"):
    print("Dose drop summary saved to: outputs/dose_drop_summary.csv")

