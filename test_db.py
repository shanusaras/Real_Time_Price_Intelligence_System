import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Try different connection string formats
db_configs = [
    "mysql+pymysql://root@localhost:3306/price_intelligence_v2",
    "mysql+pymysql://root@127.0.0.1:3306/price_intelligence_v2",
    "mysql+pymysql://localhost:3306/price_intelligence_v2"
]

for url in db_configs:
    try:
        print(f"Trying {url}...")
        engine = create_engine(url)
        with engine.connect() as conn:
            print("✅ Successfully connected!")
            break
    except Exception as e:
        print(f"❌ Failed: {str(e)}")