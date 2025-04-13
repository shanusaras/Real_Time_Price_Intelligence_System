from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_html(search_term):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    url = f"https://www.flipkart.com/search?q={search_term}"
    driver.get(url)

    time.sleep(3)  # Wait for JS content to load
    html = driver.page_source
    driver.quit()

    return html

if __name__ == "__main__":
    print("📡 Starting HTML fetch...")
    html = get_html("laptop")
    print("✅ HTML fetch complete.")
    print("🔍 Preview of content:\n")
    print(html[:1000])


