from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

# Function to fetch HTML content for a given search term from Flipkart
# It loops through multiple pages and combines the HTML

def get_html(search_term, num_pages=120):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    all_html = ""

    for page in range(1, num_pages + 1):
        print(f"Fetching page {page} for '{search_term}'")
        url = f"https://www.flipkart.com/search?q={search_term}&page={page}"
        driver.get(url)

        # Debug: Print the current URL
        print(f"Current URL: {driver.current_url}")

        # Wait for main product container to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".s1Q9rs"))  # Updated selector for product links
            )
        except Exception as e:
            print(f"⚠️ Timeout waiting for page {page} to load: {e}")
            print(driver.page_source)  # Debug: Print the page source for analysis
            continue

        # Debug: Print the page source for verification
        print("Page source fetched:")
        print(driver.page_source[:1000])  # Print the first 1000 characters for debugging

        time.sleep(random.uniform(2.5, 4.5))  # slight delay to avoid bot detection
        all_html += driver.page_source

    driver.quit()
    return all_html