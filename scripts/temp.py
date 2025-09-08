# scripts/clean_vaccine_introduction.py
import pandas as pd

# File paths
vaccine_schedule_file = r"data/raw/vaccine_schedule.xlsx"
vaccine_intro_file = r"data/raw/vaccine_introduction.xlsx"
output_file = r"data/processed/vaccine_introduction_cleaned.csv"

# Load datasets
vaccine_schedule = pd.read_excel(vaccine_schedule_file)
vaccine_intro = pd.read_excel(vaccine_intro_file)

# Normalize column names
vaccine_schedule.columns = vaccine_schedule.columns.str.strip().str.lower()
vaccine_intro.columns = vaccine_intro.columns.str.strip().str.lower()

# Rename columns in vaccine_intro to match schedule
vaccine_intro.rename(columns={"description": "vaccinecode"}, inplace=True)

# Clean string columns: strip spaces & uppercase
for df, cols in [(vaccine_schedule, ['iso_3_code','vaccinecode']),
                 (vaccine_intro, ['iso_3_code','vaccinecode'])]:
    for col in cols:
        df[col] = df[col].astype(str).str.strip().str.upper()

# Identify mismatched vaccinecodes
mismatch = vaccine_intro.merge(
    vaccine_schedule[['iso_3_code', 'year', 'vaccinecode']],
    on=['iso_3_code','year','vaccinecode'],
    how='left',
    indicator=True
).query('_merge == "left_only"')

if not mismatch.empty:
    print("Found mismatched vaccine codes. Mapping them automatically...")

    # Create mapping from mismatches to closest match in schedule
    # Here, we match by iso_3_code + year; choose first matching vaccinecode from schedule
    mapping = {}
    for idx, row in mismatch.iterrows():
        iso, yr = row['iso_3_code'], row['year']
        possible = vaccine_schedule[(vaccine_schedule['iso_3_code']==iso) &
                                    (vaccine_schedule['year']==yr)]
        if not possible.empty:
            # Take first schedule vaccinecode as replacement
            mapping[row['vaccinecode']] = possible['vaccinecode'].values[0]

    # Apply mapping
    vaccine_intro['vaccinecode'] = vaccine_intro['vaccinecode'].replace(mapping)

# Keep only valid rows after mapping
valid_intro = pd.merge(
    vaccine_intro,
    vaccine_schedule[['iso_3_code','year','vaccinecode']],
    on=['iso_3_code','year','vaccinecode'],
    how='inner'
)

# Print stats
print(f"Original rows: {len(vaccine_intro)}")
print(f"Valid rows after cleaning: {len(valid_intro)}")
print(f"Removed invalid rows: {len(vaccine_intro) - len(valid_intro)}")

# Save cleaned CSV
valid_intro.to_csv(output_file, index=False)
print(f"Cleaned vaccine introduction CSV saved successfully at:\n{output_file}")
