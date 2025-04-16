#!/usr/bin/env python3
# main.py — Multi-Category Price Intelligence Scraper

import yaml
import time
import random
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from modules.fetcher import get_html
from modules.parser import parse_data, save_to_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

class PriceIntelligenceScraper:
    def __init__(self):
        self.config = self.load_config()
        self.setup_directories()
        self.last_request_time = 0
        self.min_delay = self.config['scraping_config']['delay_between_pages'][0]
        self.max_delay = self.config['scraping_config']['delay_between_pages'][1]

    @staticmethod
    def load_config():
        config_path = Path('flipkart_scraper/config/categories.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def setup_directories():
        dirs = ['data', 'data/raw', 'data/processed', 'logs']
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def apply_rate_limiting(self):
        """Ensure minimum delay between requests"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        self.last_request_time = time.time()

    def scrape_category(self, category_name, category_config):
        """Scrape products for a specific category"""
        logging.info(f"Starting scrape for category: {category_name}")
        
        try:
            # Apply rate limiting
            self.apply_rate_limiting()
            
            # Fetch HTML content
            html = get_html(
                category_config['search_term'],
                num_pages=self.config['scraping_config']['pages_per_category']
            )
            
            if not html:
                logging.error(f"Failed to fetch HTML for {category_name}")
                return None
            
            # Parse the data
            records = parse_data(html, category=category_name)
            logging.info(f"✅ Parsed {len(records)} records for {category_name}")
            
            # Save to database
            if records:
                self.db_manager.save_product_data(records)
                
                # Also save to CSV for backup/analysis
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                df = pd.DataFrame(records)
                df.to_csv(f"data/raw/{category_name}_{timestamp}.csv", index=False)
                logging.info(f"📁 Saved {category_name} data to CSV and database")
                
                return len(records)
            
        except Exception as e:
            logging.error(f"Error scraping {category_name}: {str(e)}")
            return None

    def run(self):
        """Run the scraper for all configured categories"""
        total_records = 0
        successful_categories = 0
        
        for category_name, category_config in self.config['categories'].items():
            records_count = self.scrape_category(category_name, category_config)
            
            if records_count:
                total_records += records_count
                successful_categories += 1
        
        logging.info(f"✨ Scraping completed! Processed {successful_categories} categories")
        logging.info(f"📊 Total records collected: {total_records}")

def main():
    scraper = PriceIntelligenceScraper()
    scraper.run()

if __name__ == "__main__":
    main()