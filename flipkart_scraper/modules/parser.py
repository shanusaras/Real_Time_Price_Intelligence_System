
from bs4 import BeautifulSoup
import yaml
from modules.utils import extract_with_fallback



# Load the CSS selectors from config file (YAML format)
def load_selectors():
    with open("flipkart_scraper/config/selectors.yaml", "r") as f:
        return yaml.safe_load(f)
    

# Parse relevant product info from raw HTML using selectors
# Returns list of dicts with product info

def parse_data(html, category="unknown"):
    soup = BeautifulSoup(html, "html.parser")
    selectors = load_selectors()

    # Extract fields using fallback logic (tries multiple selectors)
    titles = extract_with_fallback(soup, selectors["product_title"])
    prices = extract_with_fallback(soup, selectors["product_price"])
    ratings = extract_with_fallback(soup, selectors["product_rating"])
    reviews = extract_with_fallback(soup, selectors["num_reviews"])
    discounts = extract_with_fallback(soup, selectors["discount"])

    # Use minimum length to align records and avoid index errors
    min_len = min(len(titles), len(prices), len(ratings), len(reviews), len(discounts))

    return [{
        "Product Name": titles[i],
        "Price": prices[i],
        "Rating": ratings[i],
        "Reviews": reviews[i],
        "Discount": discounts[i],
        "Category": category
    } for i in range(min_len)]