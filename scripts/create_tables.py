import pymysql
from sqlalchemy import create_engine, text

# Database connection
user = "root"
password = "munny%40ridhi1701"  # URL-encoded
host = "localhost"
database = "vaccination_db"

try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    with engine.connect() as conn:
        # --- coverage table ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS coverage (
            code VARCHAR(20),
            name VARCHAR(255),
            year INT,
            antigen VARCHAR(50),
            antigen_description VARCHAR(255),
            coverage_category VARCHAR(50),
            coverage_category_description VARCHAR(255),
            target_number FLOAT,
            doses FLOAT,
            coverage FLOAT
        );
        """))

        # --- incidence table ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS incidence (
            code VARCHAR(20),
            name VARCHAR(255),
            year INT,
            disease VARCHAR(50),
            disease_description VARCHAR(255),
            denominator VARCHAR(50),
            incidence_rate FLOAT
        );
        """))

        # --- reported_cases table ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reported_cases (
            code VARCHAR(20),
            name VARCHAR(255),
            year INT,
            disease VARCHAR(50),
            disease_description VARCHAR(255),
            cases INT
        );
        """))

        # --- vaccine_introduction table ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS vaccine_introduction (
            iso_3_code VARCHAR(20),
            countryname VARCHAR(255),
            who_region VARCHAR(50),
            year INT,
            description VARCHAR(255),
            intro VARCHAR(50)
        );
        """))

        # --- vaccine_schedule table ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS vaccine_schedule (
            iso_3_code VARCHAR(20),
            countryname VARCHAR(255),
            who_region VARCHAR(50),
            year INT,
            vaccinecode VARCHAR(50),
            vaccine_description VARCHAR(255),
            schedulerounds FLOAT,
            targetpop VARCHAR(50),
            targetpop_description VARCHAR(255),
            geoarea VARCHAR(50),
            ageadministered VARCHAR(50)
        );
        """))

    print("✅ All tables created successfully!")

except Exception as e:
    print("❌ Failed to create tables:", e)
