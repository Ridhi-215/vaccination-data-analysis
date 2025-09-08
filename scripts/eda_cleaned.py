# scripts/eda_cleaned.py
import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

os.makedirs("outputs/eda_cleaned_plots", exist_ok=True)

# load
proc = "data/processed"
coverage = pd.read_csv(f"{proc}/coverage.csv")
incidence = pd.read_csv(f"{proc}/incidence.csv")
reported = pd.read_csv(f"{proc}/reported_cases.csv")

# unify lowercase
for df in (coverage, incidence, reported):
    df.columns = [c.lower() for c in df.columns]

# --- BASIC CLEANING ---
# 1) Remove rows with impossible negatives for numeric fields
coverage_clean = coverage.copy()
coverage_clean.loc[:, 'doses'] = pd.to_numeric(coverage_clean['doses'], errors='coerce')
coverage_clean.loc[:, 'target_number'] = pd.to_numeric(coverage_clean['target_number'], errors='coerce')
coverage_clean = coverage_clean[(coverage_clean['doses'].isna()) | (coverage_clean['doses'] >= 0)]
coverage_clean = coverage_clean[(coverage_clean['target_number'].isna()) | (coverage_clean['target_number'] >= 0)]

# 2) Flag/clean coverage outliers
coverage_clean.loc[:, 'coverage'] = pd.to_numeric(coverage_clean['coverage'], errors='coerce')
# Keep rows with coverage between 0 and 100 by default; keep >100 but flagged
coverage_clean['coverage_flag'] = np.where((coverage_clean['coverage'] < 0) | (coverage_clean['coverage'] > 100), 'outlier', 'ok')

# 3) Clean reported cases: convert to numeric, drop negatives
reported_clean = reported.copy()
reported_clean['cases'] = pd.to_numeric(reported_clean['cases'], errors='coerce')
reported_clean = reported_clean[reported_clean['cases'] >= 0]

# 4) Parse incidence denominator and convert incidence_rate to per 100k
inc = incidence.copy()
inc['incidence_rate'] = pd.to_numeric(inc['incidence_rate'], errors='coerce')

def denom_base(s):
    if pd.isna(s):
        return np.nan
    s = str(s).lower().replace(',', '')
    m = re.search(r'per\s*([0-9]+)', s)
    if m:
        return int(m.group(1))
    # fallback: common phrases
    if 'live' in s and 'birth' in s:
        # typical is per 10,000 live births -> guess 10000
        m2 = re.search(r'per\s*10', s)
        return 10000
    return np.nan

inc['denom_base'] = inc['denominator'].apply(denom_base)
# convert to per 100k: incidence_per_100k = incidence_rate * (100000 / denom_base)
inc['incidence_per_100k'] = np.nan
mask = inc['denom_base'].notna() & inc['incidence_rate'].notna()
inc.loc[mask, 'incidence_per_100k'] = inc.loc[mask, 'incidence_rate'] * (100000.0 / inc.loc[mask, 'denom_base'])

# --- AGGREGATE country-year level (cleaned) ---
cov_agg = coverage_clean.groupby(['code','year'], as_index=False).agg(
    avg_coverage = ('coverage','mean'),
    median_coverage = ('coverage','median'),
    coverage_count = ('coverage','count'),
    doses_sum = ('doses','sum'),
    target_sum = ('target_number','sum')
)

inc_agg = inc.groupby(['code','year'], as_index=False).agg(
    avg_incidence_per_100k = ('incidence_per_100k','mean'),
    incidence_count = ('incidence_per_100k','count')
)

rep_agg = reported_clean.groupby(['code','year'], as_index=False).agg(
    total_cases = ('cases','sum')
)

merged = cov_agg.merge(inc_agg, on=['code','year'], how='outer').merge(rep_agg, on=['code','year'], how='outer')

# save merged
merged.to_csv("outputs/eda_cleaned_summary.csv", index=False)

# --- compute correlations with p-values ---
def corr_with_p(x, y):
    df = merged[[x,y]].dropna()
    if df.shape[0] < 5:
        return None
    pear_r, pear_p = stats.pearsonr(df[x], df[y])
    spear_r, spear_p = stats.spearmanr(df[x], df[y])
    return {'n': len(df), 'pearson_r': pear_r, 'pearson_p': pear_p, 'spearman_r': spear_r, 'spearman_p': spear_p}

c1 = corr_with_p('avg_coverage','avg_incidence_per_100k')
c2 = corr_with_p('avg_coverage','total_cases')

print("Correlation cleaned results:")
print("avg_coverage vs avg_incidence_per_100k:", c1)
print("avg_coverage vs total_cases:", c2)

# --- Scatter plots (log transform total_cases) ---
def scatter(x,y, fname, logy=False):
    df = merged[[x,y,'code','year']].dropna()
    if df.empty:
        print("no data for", fname); return
    plt.figure(figsize=(7,5))
    if logy:
        df = df[df[y] > 0]
        sns.scatterplot(x=df[x], y=np.log1p(df[y]), alpha=0.5)
        plt.ylabel("log(1 + {})".format(y))
    else:
        sns.scatterplot(x=df[x], y=df[y], alpha=0.5)
    plt.xlabel(x); plt.title(fname)
    plt.tight_layout()
    plt.savefig(f"outputs/eda_cleaned_plots/{fname}.png")
    plt.close()

scatter('avg_coverage','avg_incidence_per_100k','cov_vs_inc_per100k')
scatter('avg_coverage','total_cases','cov_vs_cases_log', logy=True)

# --- top problematic rows to inspect ---
# coverage > 100
bad_cov = coverage_clean[coverage_clean['coverage_flag']=='outlier'].sort_values('coverage', ascending=False).head(50)
bad_cov.to_csv("outputs/top_coverage_outliers.csv", index=False)

# negative/huge doses/target numbers
coverage_clean[coverage_clean['doses'] < 0].to_csv("outputs/negative_doses.csv", index=False)
coverage_clean[coverage_clean['target_number'] < 0].to_csv("outputs/negative_targets.csv", index=False)

print("\nSaved cleaned summary, plots and outlier lists in outputs/ (see eda_cleaned_summary.csv and eda_cleaned_plots/)")
