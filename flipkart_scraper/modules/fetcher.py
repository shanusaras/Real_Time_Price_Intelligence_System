import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse
import logging
import random
import yaml
from datetime import datetime
from pathlib import Path
from .ethical_utils import ethical_scraping_decorator, EthicalScraperConfig

# Set up logging
logger = logging.getLogger(__name__)
config = EthicalScraperConfig()
logger.setLevel(logging.INFO)
logger_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logger_format)
logger.addHandler(logger_handler)

# Load categories configuration
def load_categories():
    config_path = Path(__file__).parent.parent / 'config' / 'categories.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

categories_config = load_categories()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logger_format)
logger.addHandler(logger_handler)

def get_html(search_term, num_pages=1, min_price=None, max_price=None, max_retries=3, category=None):
    """Fetch HTML content from Flipkart with price range filters"""
    def _get_html_impl(search_term, num_pages=1, min_price=None, max_price=None, max_retries=3, category=None, url=None):
        driver = None
        retry_count = 0
        html_content = ""
        while retry_count < max_retries:
            try:
                # Initialize Chrome driver with options
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument(f'--user-agent={config.USER_AGENT}')
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.set_page_load_timeout(30)
                # Make automation less detectable
                driver.execute_cdp_cmd('Network.enable', {})
                driver.execute_cdp_cmd('Network.setBypassServiceWorker', {'bypass': True})
                driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': '''
                        Object.defineProperty(navigator, 'webdriver', { get: () => undefined })
                        window.chrome = { runtime: {} }
                        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] })
                    '''
                })
                # First navigate to Flipkart homepage and handle any popups
                driver.get('https://www.flipkart.com')
                time.sleep(random.uniform(2, 3))
                try:
                    # Try to close login popup if it appears
                    close_button = driver.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
                    close_button.click()
                    time.sleep(1)
                except:
                    pass
                # Construct search URL with price filters
                base_url = 'https://www.flipkart.com/search'
                search_params = {'q': search_term}
                if min_price:
                    search_params['price_min'] = min_price
                if max_price:
                    search_params['price_max'] = max_price
                search_url = f"{base_url}?{urllib.parse.urlencode(search_params)}"
                url = search_url
                driver.get(search_url)
                # Wait for initial page load and handle CAPTCHA if needed
                time.sleep(random.uniform(3, 5))
                # Check for CAPTCHA
                try:
                    captcha = driver.find_element(By.CSS_SELECTOR, '._25b18c')
                    logger.warning(f"CAPTCHA detected for {search_term}")
                    raise Exception("CAPTCHA detected")
                except:
                    pass
                # Process pages
                for page in range(1, num_pages + 1):
                    logger.info(f"Fetching page {page} for '{search_term}' in category: {category}")
                    # Get page content
                    page_content = driver.page_source
                    if not page_content.strip():
                        logger.warning(f"Empty page content for page {page}")
                        continue
                    html_content += page_content
                    # Navigate to next page if needed
                    if page < num_pages:
                        try:
                            next_button = driver.find_element(By.CSS_SELECTOR, 'a._1LKTO3')
                            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                            time.sleep(1)
                            next_button.click()
                            time.sleep(random.uniform(2, 3))
                        except Exception as e:
                            logger.error(f"Failed to navigate to next page: {e}")
                            break
                            pass
                    except Exception as e:
                        logger.warning(f"Could not navigate to next page: {str(e)}")
                        break
            
            logger.info(f"Successfully fetched {num_pages} pages for '{search_term}'")
            return html_content
            
        except Exception as e:
            retry_count += 1
            logger.error(f"Error fetching page {retry_count}/{max_retries}: {str(e)}")
            
            if driver:
                driver.quit()
                driver = None
            
            if retry_count < max_retries:
                logger.info(f"Retrying in {config.RATE_LIMIT} seconds...")
                time.sleep(config.RATE_LIMIT)
            else:
                logger.error(f"Failed after {max_retries} attempts")
                return ""

            # First navigate to Flipkart homepage and handle any popups
            driver.get('https://www.flipkart.com')
            time.sleep(random.uniform(2, 3))
            
            try:
                # Try to close login popup if it appears
                close_button = driver.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
                close_button.click()
                time.sleep(1)
            except:
                pass
            
            # Construct search URL with price filters
            base_url = 'https://www.flipkart.com/search'
            search_params = {'q': search_term}
            
            if min_price:
                search_params['price_min'] = min_price
            if max_price:
                search_params['price_max'] = max_price
            
            search_url = f"{base_url}?{urllib.parse.urlencode(search_params)}"
            url = search_url  # Always set the url kwarg for decorator/caching/robots.txt logic
            driver.get(search_url)
            
            # Wait for initial page load
            time.sleep(random.uniform(3, 5))
            
            all_html = ""
            for page in range(1, num_pages + 1):
                logger.info(f"Fetching page {page} for '{search_term}'")
                
                if page > 1:
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '._1LKTO3'))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(1)
                        next_button.click()
                        time.sleep(random.uniform(2, 3))
                    except Exception as e:
                        logger.error(f"Failed to navigate to next page: {e}")
                        break
                
                try:
                    # Wait for product grid to load
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._1YokD2._3Mn1Gg'))
                    )
                    
                    # Scroll through the page to load all content
                    for _ in range(3):
                        driver.execute_script("window.scrollBy(0, 500)")
                        time.sleep(1)
                    
                    driver.execute_script("window.scrollTo(0, 0)")
                    time.sleep(2)
                    
                    # Get the page source after everything is loaded
                    all_html += driver.page_source
                    
                    # Add a random delay between pages
                    time.sleep(random.uniform(4, 6))
                    
                except Exception as e:
                    logger.error(f"Error loading product grid on page {page}: {e}")
                    break
            
            # Close browser
            driver.quit()
            
            if len(all_html.strip()) > 0:
                return all_html
            else:
                raise Exception("No HTML content was retrieved")
                
        except Exception as e:
            logger.error(f"Attempt {retry_count + 1} failed: {str(e)}")
            if driver:
                driver.quit()
            
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(2 ** retry_count)  # Exponential backoff
            else:
                logger.error("All attempts failed")
                raise e

            # ... (rest of the code remains the same)