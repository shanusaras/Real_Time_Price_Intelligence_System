import requests
import json
import os
import time
import logging
from requests.exceptions import RequestException

def fetch_openfoodfacts_products(
    page_size=1000,
    max_records=25000,
    max_retries=3,
    rate_limit=0.5,
    error_log_path='data/openfoodfacts_errors.log',
):
    """
    Fetch product data from the Open Food Facts API in a robust, scalable manner.

    Args:
        page_size (int): Products per API request (max 1000).
        max_records (int): Max products to fetch.
        max_retries (int): Retry attempts per page on error.
        rate_limit (float): Seconds to wait between requests.
        error_log_path (str): Path to log errors.

    Returns:
        list: List of product dictionaries (raw API output).
    """
    products = []  # All products fetched
    page = 1       # Current API page
    errors = []    # Error messages for logging

    while len(products) < max_records:
        url = (
            f"https://world.openfoodfacts.org/cgi/search.pl?"
            f"search_simple=1&action=process&json=1&page={page}&page_size={page_size}"
        )
        success = False
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                batch = resp.json().get('products', [])
                if not batch:
                    # No more products available; exit loop
                    logging.info(f"No products found on page {page}. Stopping.")
                    success = True
                    break
                products.extend(batch)
                logging.info(
                    f"Fetched page {page} ({len(batch)} products, total so far: {len(products)})"
                )
                success = True
                break  # Success, break out of retry loop
            except RequestException as e:
                # Log error and retry with exponential backoff
                err_msg = f"Error on page {page}, attempt {attempt}: {e}"
                logging.warning(err_msg)
                errors.append(err_msg)
                time.sleep(2 ** attempt)  # Exponential backoff (2s, 4s, 8s)
        if not success:
            # If all retries failed, log and skip this page
            logging.error(
                f"Failed to fetch page {page} after {max_retries} attempts. Skipping."
            )
            errors.append(f"Failed to fetch page {page} after {max_retries} attempts.")
        page += 1
        time.sleep(rate_limit)  # Rate limiting between requests
        if len(products) >= max_records:
            break

    # Save errors to log file if any occurred
    if errors:
        with open(error_log_path, 'a', encoding='utf-8') as ef:
            for line in errors:
                ef.write(line + '\n')
        logging.info(f"Logged {len(errors)} errors to {error_log_path}")

    return products[:max_records]

if __name__ == "__main__":
    # Configure logging to output to both console and file
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('data/openfoodfacts_collection.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    # Ensure output directory exists
    os.makedirs('data', exist_ok=True)
    target_count = 25000
    # Fetch products from Open Food Facts
    products = fetch_openfoodfacts_products(max_records=target_count)
    logging.info(f"Fetched {len(products)} products from Open Food Facts.")
    # Save the full dataset to a JSON file
    with open('data/openfoodfacts_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    logging.info("Saved to data/openfoodfacts_products.json")

    # Save a small sample (first 100 records) for demo/testing
    sample_size = min(100, len(products))
    sample_products = products[:sample_size]
    with open('data/openfoodfacts_sample.json', 'w', encoding='utf-8') as f:
        json.dump(sample_products, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved a sample of {sample_size} products to data/openfoodfacts_sample.json")

    # Log a sample of the collected products for verification
    logging.info("Sample products:")
    for p in products[:3]:
        logging.info(f"- {p.get('product_name', 'N/A')} ({p.get('brands', 'N/A')}) [{p.get('categories', 'N/A')}] - {p.get('countries', 'N/A')}")
