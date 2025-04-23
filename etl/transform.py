import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

"""
ETL Transform:
- Reads raw JSON from Jumia scrape
- Cleans and normalizes
- Loads to database or exports CSV
"""

def main():
    load_dotenv()
    # DB connection parameters (if needed)
    engine = None  # Placeholder for SQLAlchemy engine

    # Load raw Jumia JSON
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data_collection', 'data', 'jumia_products.json')
    df = pd.read_json(raw_path)
    print(f"Loaded {len(df)} records from Jumia JSON.")

    # TODO: Data cleaning (e.g., drop duplicates, fill NAs)

    # Example: Export to CSV for analysis
    out_csv = os.path.join(os.path.dirname(__file__), 'output', 'jumia_products_clean.csv')
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"Clean data exported to {out_csv}")

if __name__ == '__main__':
    main()
