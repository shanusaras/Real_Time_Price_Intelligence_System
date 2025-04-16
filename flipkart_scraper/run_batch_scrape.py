print("RUNNING LATEST run_batch_scrape.py from:", __file__)
"""
Batch Scraping Script for Multi-Category Price Intelligence
- Loads all categories from categories.yaml
- Scrapes each category with proper error handling and rate limiting
- Saves raw HTML for each category in the data/ directory
- Logs progress and summary
"""
import os
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime
from modules.fetcher import get_html, categories_config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Output directory for raw HTML
DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw_html'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def main():
    categories = categories_config['categories']
    scraping_cfg = categories_config.get('scraping_config', {})
    pages_per_category = scraping_cfg.get('pages_per_category', 3)
    max_retries = scraping_cfg.get('max_retries', 3)
    delay_range = scraping_cfg.get('delay_between_pages', [3, 5])

    logger.info(f"Starting batch scrape for {len(categories)} categories...")

    for cat_name, cat_info in categories.items():
        logger.info(f"Scraping category: {cat_name}")
        search_term = cat_info['search_term']
        min_price = cat_info.get('min_price')
        max_price = cat_info.get('max_price')
        
        html = get_html(
            search_term=search_term,
            num_pages=pages_per_category,
            min_price=min_price,
            max_price=max_price,
            max_retries=max_retries,
            category=cat_name
        )
        
        if html:
            out_file = DATA_DIR / f"{cat_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"Saved HTML for {cat_name} to {out_file}")
        else:
            logger.warning(f"No HTML fetched for {cat_name}")

    logger.info("Batch scraping complete.")

if __name__ == "__main__":
    main()
