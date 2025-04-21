"""
Transform raw data loaded into MySQL. Clean, normalize, and enrich.
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


def main():
    load_dotenv()
    # DB connection
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = os.getenv('MYSQL_PORT', '3306')
    db = os.getenv('MYSQL_DATABASE')
    conn_str = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(conn_str)

    # Load raw table
    print("Reading raw products table...")
    df = pd.read_sql_table('products', engine)
    print(f"Loaded {len(df)} records.")

    # TODO: Data cleaning
    # - Convert price to numeric
    # - Parse date fields
    # - Drop duplicates
    # - Fill missing values

    # TODO: Enrichment
    # - Derive unit_price
    # - Flag categories

    # Write cleaned data to new table
    cleaned_table = 'products_clean'
    df.to_sql(cleaned_table, engine, if_exists='replace', index=False)
    print(f"Written cleaned data ({len(df)} rows) to table '{cleaned_table}'")


if __name__ == '__main__':
    main()
