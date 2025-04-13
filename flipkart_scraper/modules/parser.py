from bs4 import BeautifulSoup
import yaml

# Load YAML selector config
def load_selectors():
    with open("flipkart_scraper/config/selectors.yaml", "r") as f:
        return yaml.safe_load(f)

# Try multiple fallback CSS selectors
def extract_with_fallback(soup, selector_list):
    for selector in selector_list:
        elements = soup.select(selector)
        if elements:
            return [el.get_text(strip=True) for el in elements]
    return []

# Full parser function
def parse_data(html):
    soup = BeautifulSoup(html, "html.parser")
    selectors = load_selectors()

    titles = extract_with_fallback(soup, selectors["product_title"])
    prices = extract_with_fallback(soup, selectors["product_price"])

    # Match up titles and prices (truncate to shorter list if mismatch)
    min_len = min(len(titles), len(prices))
    titles = titles[:min_len]
    prices = prices[:min_len]

    return [{"Product Name": t, "Price": p} for t, p in zip(titles, prices)]
