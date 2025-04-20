import requests
import json
import os
import time
import logging
from requests.exceptions import RequestException

# Top 5 business-relevant categories
CATEGORIES = [
    "snacks",
    "beverages",
    "dairies",
    "personal-care",
    "dietary-supplements"
]

PAGE_SIZE = 1000  # Max per Open Food Facts API
MAX_PAGES_PER_CATEGORY = 3  # Adjust as needed for demo/quick runs
RATE_LIMIT = 0.5  # Seconds between requests
MAX_RETRIES = 3

# Data output
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(DATA_DIR, 'top_categories_products.json')
LOG_PATH = os.path.join(DATA_DIR, 'top_categories_scraping.log')

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def fetch_category_products(category, max_pages=3):
    products = []
    for page in range(1, max_pages + 1):
        url = f"https://world.openfoodfacts.org/category/{category}/{page}.json"
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                batch = resp.json().get('products', [])
                if not batch:
                    logging.info(f"No products found for {category} on page {page}. Stopping.")
                    return products
                for prod in batch:
                    prod['scraped_category'] = category  # Tag product with category
                products.extend(batch)
                logging.info(f"Fetched {len(batch)} products for {category} (page {page})")
                break  # Success
            except RequestException as e:
                logging.warning(f"Error fetching {category} page {page}, attempt {attempt}: {e}")
                time.sleep(2 ** attempt)
        else:
            logging.error(f"Failed to fetch {category} page {page} after {MAX_RETRIES} attempts.")
        time.sleep(RATE_LIMIT)
    return products

def main():
    all_products = []
    for category in CATEGORIES:
        logging.info(f"--- Scraping category: {category} ---")
        cat_products = fetch_category_products(category, max_pages=MAX_PAGES_PER_CATEGORY)
        all_products.extend(cat_products)
        logging.info(f"Total products for {category}: {len(cat_products)}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved {len(all_products)} products from top categories to {OUTPUT_PATH}")
    print(f"Scraping complete. Data saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
