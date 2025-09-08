from sqlalchemy import create_engine, text

# Database credentials
user = "root"
password = "munny%40ridhi1701"  # @ is encoded as %40
host = "localhost"
database = "vaccination_db"

# Create engine without specifying database to create it first
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/")

try:
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        print(f"✅ Database '{database}' created or already exists!")
except Exception as e:
    print("❌ Connection failed:", e)
