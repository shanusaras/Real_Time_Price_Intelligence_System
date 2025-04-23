from playwright.sync_api import sync_playwright, TimeoutError
import json
import os
import math

"""
Scrape product data from Jumia (a leading e-commerce platform in Nigeria) using Playwright
(a headless browser automation library) for reliable, JS-rendered page interactions.
"""

# Configuration
data_collection = os.path.dirname(__file__)
# Configuration: expand to 10 categories
CATEGORIES = [
    "snacks", "beverages", "dairies", "personal-care", "dietary-supplements",
    "electronics", "fashion-women", "fashion-men", "home-living", "phones-accessories"
]
# Increase to ~2000 records per category * 10 categories = ~20000 records
MAX_PRODUCTS_PER_CAT = 2000  # target per category
ITEMS_PER_PAGE = 40        # approx items per page
PAGES_PER_CAT = math.ceil(MAX_PRODUCTS_PER_CAT / ITEMS_PER_PAGE)

# Output
data_dir = os.path.join(data_collection, 'data')
os.makedirs(data_dir, exist_ok=True)
output_file = os.path.join(data_dir, 'jumia_playwright.json')


def scrape_category(page, category):
    results = []
    # Loop through pages via URL to gather products
    for page_num in range(1, PAGES_PER_CAT + 1):
        url = f"https://www.jumia.com.ng/catalog/?q={category}&page={page_num}"
        try:
            page.goto(url, timeout=60000)
        except TimeoutError as e:
            print(f"Timeout loading {url}: {e}. Skipping page {page_num} for {category}.")
            continue
        # Wait for products to load
        try:
            page.wait_for_selector("article.prd._fb", timeout=10000)
        except TimeoutError:
            print(f"No products load at {url}. Skipping.")
            continue
        items = page.query_selector_all("article.prd._fb")
        if not items:
            break
        for item in items:
            # Core fields
            name = item.query_selector("h3.name").inner_text().strip()
            price_text = item.query_selector("div.prc").inner_text().replace('₦','').replace(',','')
            try:
                price = float(price_text)
            except:
                price = None
            link = 'https://www.jumia.com.ng' + item.query_selector("a.core").get_attribute('href')
            # Additional fields
            brand_el = item.query_selector("div.brn")
            brand = brand_el.inner_text().strip() if brand_el else None
            disc_el = item.query_selector("div.bdg._dsct._fcm")
            discount_pct = int(disc_el.inner_text().replace('%','')) if disc_el else 0
            rev_el = item.query_selector("div.rev")
            rating, reviews = 0.0, 0
            if rev_el:
                txt = rev_el.inner_text().strip()
                parts = txt.split()
                rating = float(parts[0]) if parts else 0.0
                if '(' in txt:
                    reviews = int(txt.split('(')[1].rstrip(')'))
            oos_el = item.query_selector("div.sold-out")
            in_stock = not bool(oos_el)
            results.append({
                "name": name,
                "brand": brand,
                "price": price,
                "discount_pct": discount_pct,
                "rating": rating,
                "reviews": reviews,
                "in_stock": in_stock,
                "category": category,
                "link": link
            })
            if len(results) >= MAX_PRODUCTS_PER_CAT:
                break
        # stop if reached target
        if len(results) >= MAX_PRODUCTS_PER_CAT:
            break
    return results


def main():
    all_products = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0")
        # increase navigation timeout to 60s
        page.set_default_navigation_timeout(60000)
        for cat in CATEGORIES:
            print(f"Scraping category: {cat}")
            prods = scrape_category(page, cat)
            print(f"Found {len(prods)} products in '{cat}'")
            all_products.extend(prods)
        browser.close()
    print(f"Total scraped products: {len(all_products)}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {output_file}")


if __name__ == '__main__':
    main()
