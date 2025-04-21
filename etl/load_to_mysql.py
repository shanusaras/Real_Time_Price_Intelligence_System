import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

"""
Load full JSON dataset into MySQL (Phase 2 ETL loader)
"""

def main():
    load_dotenv()
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = os.getenv('MYSQL_PORT', '3306')
    db = os.getenv('MYSQL_DATABASE')

    conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(conn_str)

    # Load JSON data from data_collection
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data_collection', 'data', 'all_products_openfoodfacts.json')
    print(f"Loading JSON data from: {json_path}")
    df = pd.read_json(json_path, encoding='utf-8')
    print(f"Loaded {len(df)} records.")

    # Bulk insert
    table_name = 'products'
    print(f"Inserting into MySQL table '{table_name}'...")
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)
    print(f"Successfully inserted {len(df)} records into '{table_name}' table.")

if __name__ == '__main__':
    main()
