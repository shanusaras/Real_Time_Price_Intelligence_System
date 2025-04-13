import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from modules.fetcher import get_html
from modules.parser import parse_data
import pandas as pd
import logging
import os

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/scraper.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    print("Starting scraper...")


    try:      
        html = get_html("laptop")
        print("✅ HTML fetched.")

        data = parse_data(html)
        print(f"✅Parsed {len(data)} records.")
        
        if not data:
            print("❌ No data found.")
            logging.warning("⚠️ No data extracted from Flipkart.")
            return

        df = pd.DataFrame(data)

        # ✅ Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Save to CSV
        output_path = "data/flipkart_products.csv"
        df.to_csv(output_path, index=False)

        print(f"✅ Data saved to {output_path}")
        logging.info(f"✅ Scraped {len(df)} rows and saved to {output_path}")
        

    except Exception as e:
        logging.error(f"❌ Error occurred during scraping: {str(e)}")
        print("❌ Something went wrong. Check logs/scraper.log")

if __name__ == "__main__":
    main()
