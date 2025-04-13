from modules.fetcher import get_html
from modules.parser import parse_data
import pandas as pd
import logging
import os
import time
import random

# List of categories to scrape in Batch 1
batch_1_terms = [
    "laptop", "smartphone", "tablet", "smartwatch", "monitor",
    "keyboard", "mouse", "tv"
]

# Ensure data and log directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Set up logging to capture success/errors in a log file
logging.basicConfig(
    filename="logs/scraper_batch_1.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to scrape all categories in Batch 1
def run_batch_1():
    total_records = 0
    for term in batch_1_terms:
        print(f"\n🔍 Scraping: {term}")
        try:
            html = get_html(term, num_pages=120)  # Fetch 120 pages for each category
            logging.info(f"{term} → HTML fetched")
            print(f"✅ HTML fetched for {term}")

            data = parse_data(html, category=term)  # Extract relevant product fields
            print(f"✅ Parsed {len(data)} records for {term}")
            total_records += len(data)

            df = pd.DataFrame(data)
            out_path = f"data/{term}_products.csv"  # Save each category separately
            df.to_csv(out_path, index=False)
            logging.info(f"{term} → Saved {len(df)} rows")

            time.sleep(random.uniform(30, 60))  # cooldown delay to reduce ban risk


        except Exception as e:
            logging.error(f"{term} → ERROR: {str(e)}")
            print(f"❌ Failed for {term}: {e}")

    print(f"\n✅ Batch 1 done. Total: {total_records} records")

if __name__ == "__main__":
    print("Running BATCH 1 (8 categories × 120 pages)...")
    run_batch_1()
