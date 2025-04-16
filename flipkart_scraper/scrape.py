from modules.fetcher import get_html
from modules.parser import parse_data, save_to_database
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def scrape_products(search_term, category=None, num_pages=1):
    """
    Main function to scrape products from Flipkart
    Args:
        search_term: Product or category to search for
        category: Category to assign to products (defaults to search_term if None)
        num_pages: Number of pages to scrape (default 1)
    """
    try:
        logger.info(f"Starting scrape for '{search_term}' ({num_pages} pages)")
        
        # Get HTML content
        html_content = get_html(search_term, num_pages)
        if not html_content:
            logger.error("Failed to fetch HTML content")
            return False

        # Parse product data
        category = category or search_term
        products_data = parse_data(html_content, category=category)
        if not products_data:
            logger.error("No products found in HTML content")
            return False

        logger.info(f"Found {len(products_data)} products")

        # Save to database
        success = save_to_database(products_data)
        return success

    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape products from Flipkart")
    parser.add_argument("search_term", help="Product or category to search for")
    parser.add_argument("--category", help="Category to assign to products")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    
    args = parser.parse_args()
    
    success = scrape_products(args.search_term, args.category, args.pages)
    sys.exit(0 if success else 1)
