from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

# Function to fetch HTML content for a given search term from Flipkart
# It loops through multiple pages and combines the HTML

def get_html(search_term, num_pages=120):
    options = Options()
    options.add_argument("--headless") # run Chrome in headless mode (no GUI)
    options.add_argument("user-agent=Mozilla/5.0") # mimic real browser user-agent

    driver = webdriver.Chrome(options=options)
    all_html = ""

    for page in range(1, num_pages + 1):
        print(f"Fetching page {page} for '{search_term}'")
        url = f"https://www.flipkart.com/search?q={search_term}&page={page}"
        driver.get(url)

        time.sleep(random.uniform(2.5, 5))   # random delay to avoid bot detection
        all_html += driver.page_source

    driver.quit()
    return all_html


# Test block to fetch and preview HTML (first 1000 chars only)
if __name__ == "__main__":
    print("Starting HTML fetch...")
    html = get_html("laptop", num_pages=2)  # testing with 2 pages only
    print("✅ HTML fetch complete.")
    print("Preview of content:\n")
    print(html[:1000])
