import pandas as pd
import os

# Paths
raw_path = "data/raw/"
processed_path = "data/processed/"
os.makedirs(processed_path, exist_ok=True)

def clean_year(df):
    """Drop rows with missing year and convert year to integer."""
    df = df.dropna(subset=["YEAR"])
    df["YEAR"] = df["YEAR"].astype(int)
    return df

# --- Coverage Data ---
coverage = pd.read_excel(raw_path + "coverage.xlsx")
coverage = coverage.drop(columns=["GROUP"])
coverage = clean_year(coverage)
coverage.columns = coverage.columns.str.lower()
coverage.to_csv(processed_path + "coverage.csv", index=False)

# --- Incidence Data ---
incidence = pd.read_excel(raw_path + "incidence.xlsx")
incidence = incidence.drop(columns=["GROUP"])
incidence = clean_year(incidence)
incidence.columns = incidence.columns.str.lower()
incidence.to_csv(processed_path + "incidence.csv", index=False)

# --- Reported Cases ---
reported = pd.read_excel(raw_path + "reported_cases.xlsx")
reported = reported.drop(columns=["GROUP"])
reported = clean_year(reported)
reported["CASES"] = reported["CASES"].fillna(0).astype(int)
reported.columns = reported.columns.str.lower()
reported.to_csv(processed_path + "reported_cases.csv", index=False)

# --- Vaccine Introduction ---
intro = pd.read_excel(raw_path + "vaccine_introduction.xlsx")
intro = clean_year(intro)
intro.columns = intro.columns.str.lower()
intro.to_csv(processed_path + "vaccine_introduction.csv", index=False)

# --- Vaccine Schedule ---
schedule = pd.read_excel(raw_path + "vaccine_schedule.xlsx")
schedule = schedule.drop(columns=["SOURCECOMMENT"], errors="ignore")
schedule = clean_year(schedule)
schedule.columns = schedule.columns.str.lower()
schedule.to_csv(processed_path + "vaccine_schedule.csv", index=False)

print("✅ Cleaning complete! Clean CSVs saved in data/processed/ (years are now integers)")
