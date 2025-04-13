from modules.fetcher import get_html
from modules.parser import parse_data
import pandas as pd
import logging
import os
import time
import random

# List of categories to scrape in Batch 2
batch_2_terms = [
    "printer", "camera", "refrigerator", "washing machine", "air conditioner",
    "microwave", "router"
]

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Logging for Batch 2 scraping
logging.basicConfig(
    filename="logs/scraper_batch_2.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to scrape all Batch 2 categories

def run_batch_2():
    total_records = 0
    for term in batch_2_terms:
        print(f"\nScraping: {term}")
        try:
            html = get_html(term, num_pages=120)
            logging.info(f"{term} → HTML fetched")
            print(f"✅ HTML fetched for {term}")

            data = parse_data(html, category=term)
            print(f"✅ Parsed {len(data)} records for {term}")
            total_records += len(data)

            df = pd.DataFrame(data)
            out_path = f"data/{term}_products.csv"
            df.to_csv(out_path, index=False)
            logging.info(f"{term} → Saved {len(df)} rows")

            time.sleep(random.uniform(30, 60))  # Anti-ban delay

        except Exception as e:
            logging.error(f"{term} → ERROR: {str(e)}")
            print(f"❌ Failed for {term}: {e}")

    print(f"\n✅ Batch 2 done. Total: {total_records} records")

if __name__ == "__main__":
    print("Running BATCH 2 (7 categories × 120 pages)...")
    run_batch_2()
