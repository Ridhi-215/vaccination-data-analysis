import pandas as pd

# Load each dataset (Excel files from data/raw/)
coverage = pd.read_excel("data/raw/coverage.xlsx")
incidence = pd.read_excel("data/raw/incidence.xlsx")
reported = pd.read_excel("data/raw/reported_cases.xlsx")
intro = pd.read_excel("data/raw/vaccine_intro.xlsx")
schedule = pd.read_excel("data/raw/vaccine_schedule.xlsx")

# Print first few rows to check structure
print("Coverage:")
print(coverage.head(), "\n")

print("Incidence:")
print(incidence.head(), "\n")

print("Reported Cases:")
print(reported.head(), "\n")

print("Vaccine Introduction:")
print(intro.head(), "\n")

print("Vaccine Schedule:")
print(schedule.head(), "\n")
