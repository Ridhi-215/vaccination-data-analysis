import pandas as pd
from sqlalchemy import create_engine, text

# Database connection
user = "root"
password = "munny%40ridhi1701"  # URL-encoded
host = "localhost"
database = "vaccination_db"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

def load_csv_to_table(csv_path, table_name, col_lengths=None):
    """
    Load CSV into MySQL table.
    :param csv_path: Path to the CSV file
    :param table_name: Target table name in MySQL
    :param col_lengths: Optional dict {column_name: max_length} to truncate strings
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Trim string columns if col_lengths is provided
        if col_lengths:
            for col, max_len in col_lengths.items():
                if col in df.columns:
                    df[col] = df[col].astype(str).str[:max_len]
        
        df = df.where(pd.notnull(df), None)  # Replace NaN with None
        
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"✅ {table_name} loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load {table_name}: {e}")

# --- Load tables with proper string length handling ---
load_csv_to_table("data/processed/coverage.csv", "coverage", {
    "code": 20, "name": 255, "antigen": 50, "antigen_description": 255,
    "coverage_category": 50, "coverage_category_description": 255
})

load_csv_to_table("data/processed/incidence.csv", "incidence", {
    "code": 20, "name": 255, "disease": 50, "disease_description": 255,
    "denominator": 50
})

load_csv_to_table("data/processed/reported_cases.csv", "reported_cases", {
    "code": 20, "name": 255, "disease": 50, "disease_description": 255
})

load_csv_to_table("data/processed/vaccine_introduction.csv", "vaccine_introduction", {
    "iso_3_code": 20, "countryname": 255, "who_region": 50, "description": 255, "intro": 50
})

load_csv_to_table("data/processed/vaccine_schedule.csv", "vaccine_schedule", {
    "iso_3_code": 20, "countryname": 255, "who_region": 50,
    "vaccinecode": 50, "vaccine_description": 255,
    "targetpop": 50, "targetpop_description": 255,
    "geoarea": 50, "ageadministered": 50
})
