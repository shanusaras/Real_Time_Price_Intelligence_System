#!/usr/bin/env python3
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_html(search_term, num_pages=1, min_price=None, max_price=None):
    """Fetch HTML content from Flipkart"""
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Initialize webdriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Construct URL with price filters
        base_url = "https://www.flipkart.com/search"
        params = {"q": search_term}
        if min_price is not None:
            params["p[]=facets.price_range.from%3D{}".format(min_price)]
        if max_price is not None:
            params["p[]=facets.price_range.to%3D{}".format(max_price)]
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        logging.info(f"Fetching URL: {url}")
        
        # Get the page
        driver.get(url)
        time.sleep(2)  # Wait for dynamic content to load
        
        # Get the HTML content
        html_content = driver.page_source
        driver.quit()
        
        return html_content
        
    except Exception as e:
        logging.error(f"Error fetching HTML: {str(e)}")
        return None

def test_scraper():
    """Test the scraper"""
    try:
        # Test laptops category with price range
        search_term = "laptop"
        min_price = 30000
        max_price = 100000
        
        # Get HTML content
        html = get_html(
            search_term=search_term,
            min_price=min_price,
            max_price=max_price
        )
        
        if html:
            logging.info("✅ Successfully fetched HTML content")
            # Save HTML to file for inspection
            with open("test_output.html", "w", encoding="utf-8") as f:
                f.write(html)
            logging.info("✅ Saved HTML content to test_output.html")
        else:
            logging.error("❌ Failed to get HTML content")
            
    except Exception as e:
        logging.error(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_scraper()
