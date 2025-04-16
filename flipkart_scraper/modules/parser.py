from bs4 import BeautifulSoup
import yaml
from datetime import datetime
import re
import logging
from .utils import extract_with_fallback
from .db_operations import ScraperDBManager

logger = logging.getLogger(__name__)

def load_selectors():
    """Load the CSS selectors from config file (YAML format)"""
    with open("flipkart_scraper/config/selectors.yaml", "r") as f:
        return yaml.safe_load(f)

def clean_price(price_str):
    """Extract numeric price from string"""
    if not price_str:
        return None
    # Remove currency symbol, commas, and whitespace
    price_num = re.sub(r'[^0-9.]', '', price_str)
    try:
        return float(price_num)
    except ValueError:
        return None

def extract_review_count(review_str):
    """Extract numeric review count from string"""
    if not review_str:
        return None
    # Extract numbers from strings like "1,234 Reviews"
    match = re.search(r'([\d,]+)\s*(?:Reviews?|Ratings?)', review_str)
    if match:
        try:
            return int(match.group(1).replace(',', ''))
        except ValueError:
            return None
    return None

def extract_discount_percentage(discount_str):
    """Extract discount percentage from string"""
    if not discount_str:
        return None
    # Extract numbers from strings like "40% off"
    match = re.search(r'(\d+)%', discount_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def clean_features(features_list):
    """Clean and combine feature strings"""
    if not features_list:
        return None
    # Remove duplicates and empty strings
    features = [f.strip() for f in features_list if f and f.strip()]
    return '\n'.join(features) if features else None

def clean_rating(rating_str):
    """Extract numeric rating from string"""
    if not rating_str:
        return None
    try:
        return float(rating_str.strip())
    except ValueError:
        return None

def extract_brand_from_title(title):
    """Try to extract brand from product title if not found separately"""
    if not title:
        return None
    # Common pattern: Brand starts at beginning until space
    brand_match = re.match(r'^([A-Za-z0-9]+)', title)
    if brand_match:
        return brand_match.group(1)
    return None

def parse_data(html, category="unknown"):
    """Parse product information from HTML content
    Returns list of dicts matching our database schema"""
    soup = BeautifulSoup(html, "html.parser")
    selectors = load_selectors()
    current_time = datetime.utcnow()

    # Extract fields using fallback logic
    titles = extract_with_fallback(soup, selectors["product_title"])
    prices = extract_with_fallback(soup, selectors["product_price"])
    original_prices = extract_with_fallback(soup, selectors["original_price"])
    discounts = extract_with_fallback(soup, selectors["discount_percentage"])
    brands = extract_with_fallback(soup, selectors["product_brand"])
    descriptions = extract_with_fallback(soup, selectors["product_description"])
    features = extract_with_fallback(soup, selectors["product_features"])
    ratings = extract_with_fallback(soup, selectors["product_rating"])
    reviews = extract_with_fallback(soup, selectors["review_count"])
    urls = extract_with_fallback(soup, selectors["product_url"])

    # Use minimum length to align records and avoid index errors
    min_len = min(
        len(titles), len(prices),
        len(ratings) or float('inf'),
        len(reviews) or float('inf'),
        len(brands) or float('inf'),
        len(descriptions) or float('inf'),
        len(urls) or float('inf')
    )

    products = []
    for i in range(min_len):
        # Get brand from dedicated field or extract from title
        brand = brands[i] if i < len(brands) else extract_brand_from_title(titles[i])
        
        # Clean and validate price
        price = clean_price(prices[i])
        if not price:
            continue

        # Build product record
        product = {
            "name": titles[i].strip(),
            "category": category,
            "brand": brand.strip() if brand else None,
            "description": descriptions[i].strip() if i < len(descriptions) else None,
            "features": clean_features(features[i]) if i < len(features) else None,
            "created_at": current_time,
            "updated_at": current_time
        }

        # Add rating and review count
        if i < len(ratings):
            rating = clean_rating(ratings[i])
            if rating:
                product["rating"] = rating

        if i < len(reviews):
            review_count = extract_review_count(reviews[i])
            if review_count:
                product["review_count"] = review_count

        # Build price history record
        price_history = {
            "price": price,
            "currency": "INR",  # Flipkart uses Indian Rupees
            "timestamp": current_time,
            "source": "flipkart"
        }

        # Add original price and discount
        if i < len(original_prices):
            original_price = clean_price(original_prices[i])
            if original_price:
                price_history["original_price"] = original_price

        if i < len(discounts):
            discount = extract_discount_percentage(discounts[i])
            if discount:
                price_history["discount_percentage"] = discount

        # Add URL for competitor reference
        if i < len(urls):
            url = urls[i]
            if not url.startswith('http'):
                url = f"https://www.flipkart.com{url}"
            price_history["url"] = url

        products.append({
            "product": product,
            "price_history": price_history
        })

    return products

def save_to_database(products_data):
    """Save parsed product data to database
    Args:
        products_data: List of product dictionaries from parse_data
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        db_manager = ScraperDBManager()
        db_manager.save_product_data(products_data)
        logger.info(f"Successfully saved {len(products_data)} products to database")
        return True
    except Exception as e:
        logger.error(f"Failed to save products to database: {str(e)}")
        return False