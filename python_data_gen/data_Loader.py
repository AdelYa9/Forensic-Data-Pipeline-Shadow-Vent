import pandas as pd
from sqlalchemy import create_engine

# 1. The Connection String (The 'Key' to the Vault)
# Format: postgresql://username:password@localhost:5432/database_name
DATABASE_URL = 'postgresql://postgres:password@localhost:5432/vaell_inc'

def load_vaell_data():
    try:
        # 2. Extract: Read the "Evidence" CSV
        print("--- [EXTRACT] Reading 'vaell_raw_data.csv' ---")
        df = pd.read_csv("vaell_raw_data.csv")
        # ---Convert 0/1 to True/False ---
        # This tells the 'Strict Librarian' exactly what she wants to hear.
        df['is_synthetic'] = df['is_synthetic'].astype(bool)
        # 3. Load: "Push" the data into the PostgreSQL table
        # Used SQLAlchemy to handle the translation between Pandas and SQL.
        engine = create_engine(DATABASE_URL)
        
        print(f"--- [LOAD] Injecting {len(df)} records into 'vaell_customers' ---")
        
        # 'if_exists=append' adds to the table. 'index=False' prevents extra ID columns.
        df.to_sql('vaell_customers', engine, if_exists='append', index=False)
        
        print("\n[SUCCESS] The Vaell Inc. Ledger has been secured in The Vault.")
        
    except Exception as e:
        print(f"\n[ERROR] The Vault rejected the connection: {e}")

if __name__ == "__main__":
    load_vaell_data()
