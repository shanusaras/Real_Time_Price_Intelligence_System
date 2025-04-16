import time
import random
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from .proxies import get_random_proxy
import json
import os

def get_html(search_term, num_pages=1, min_price=None, max_price=None, max_retries=3, category=None):
    """
    Fetch HTML content from Flipkart for a given search term and price range.
    """
    base_url = "https://www.flipkart.com/search"
    params = {
        "q": search_term
    }
    if min_price is not None:
        params["p%5B%5D"] = f"min-{min_price}"
    if max_price is not None:
        params["p%5B%5D"] = f"max-{max_price}"

    # Build the search URL
    import urllib.parse
    query_string = urllib.parse.urlencode(params, doseq=True)
    url = f"{base_url}?{query_string}"

    logging.info(f"Fetching URL: {url}")

    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # DISABLED for debugging anti-bot/captcha
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # Pick a random proxy for this session
    proxy = get_random_proxy()
    options.add_argument(f'--proxy-server={proxy}')

    # Path to Flipkart cookies file
    cookies_path = os.path.join(os.path.dirname(__file__), '..', 'flipkart_cookies.json')

    html = ""
    retry_count = 0
    while retry_count < max_retries:
        try:
            driver = uc.Chrome(options=options)
            driver.get("https://www.flipkart.com")  # Load base domain first for cookie injection

            # Load cookies from file and add to browser
            if os.path.exists(cookies_path):
                with open(cookies_path, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    # Selenium requires expiry to be int, not float
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        pass  # Ignore cookie errors (domain mismatch, etc.)

            driver.get(url)

            # Wait for product cards to load (robust selector for laptops & most categories)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            product_card_selector = "div._1AtVbE"  # Main product card container
            try:
                WebDriverWait(driver, 18).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, product_card_selector))
                )
            except Exception as wait_err:
                logging.warning(f"Product cards did not appear in time: {wait_err}")
            # Scroll to bottom to trigger lazy loading
            try:
                for _ in range(3):
                    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                    time.sleep(1.5)
            except Exception as scroll_err:
                logging.warning(f"Scrolling failed: {scroll_err}")
            time.sleep(random.uniform(1, 2))  # Small extra wait

            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            logging.error(f"Attempt {retry_count + 1} failed: {e}")
            retry_count += 1
            time.sleep(2 ** retry_count)
            try:
                driver.quit()
            except Exception:
                pass

    logging.error("All attempts to fetch HTML failed.")
    return None
