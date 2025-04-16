# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import sys
print("DEBUG: CWD =", os.getcwd())
print("DEBUG: sys.path =", sys.path)
print("DEBUG: __file__ =", __file__)
with open(__file__, 'r', encoding='utf-8') as f:
    print("DEBUG: First 10 lines of file:")
    for i, line in enumerate(f):
        if i >= 10: break
        print(line.rstrip())

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from modules.fetcher import get_html
from modules.parser import parse_data

print("RUNNING test_scraper.py FROM:", __file__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_single_category():
    """Test scraping a single category with price filters"""
    try:
        # Test laptops category with price range
        search_term = "laptop"
        min_price = 30000
        max_price = 100000
        num_pages = 1

        # Get HTML content
        html = get_html(
            search_term=search_term,
            num_pages=num_pages,
            min_price=min_price,
            max_price=max_price
        )

        if html:
            print("\n===== HTML SNIPPET (first 2000 chars) =====\n" + html[:2000] + "\n==========================================\n")
            # Parse the HTML content
            products = parse_data(html, category="laptops")
            if products:
                logging.info(f"✅ Successfully scraped {len(products)} laptop records")
                for product in products[:3]:  # Show first 3 products
                    logging.info(f"Found: {product['product']['name']} - ₹{product['price_history']['price']}")
            else:
                logging.error("❌ No products found in the HTML content")
        else:
            logging.error("❌ Failed to get HTML content")

    except Exception as e:
        logging.error(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_single_category()
