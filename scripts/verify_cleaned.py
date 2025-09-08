import pandas as pd
import os

# Paths
processed_path = "data/processed/"

for file in os.listdir(processed_path):
    if file.endswith(".csv"):
        print(f"\n=== {file} ===")
        df = pd.read_csv(processed_path + file)

        # Shape and columns
        print("Shape:", df.shape)
        print("Columns:", list(df.columns))

        # Preview first 3 rows
        print(df.head(3))

        # Missing values count
        print("\nMissing values per column:")
        print(df.isnull().sum())

        # Data types
        print("\nColumn data types:")
        print(df.dtypes)
