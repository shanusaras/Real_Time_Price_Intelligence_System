"""
Data cleaning functions for the ETL pipeline.
"""
import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: Any) -> str:
    """Clean and normalize text data."""
    if text is None:
        return ""
    if not isinstance(text, str):
        try:
            text = str(text)
        except (ValueError, TypeError):
            return ""
    # Remove extra whitespace, newlines, and normalize
    text = ' '.join(text.split())
    return text.strip()

def clean_price(price: Any) -> float:
    """Clean and convert price string to float."""
    if price is None:
        return 0.0
        
    # Handle non-string values
    if not isinstance(price, (str, int, float)):
        return 0.0
    
    # Convert to string if it's a number
    price_str = str(price).strip()
    
    # Handle 'Free' or empty string
    if not price_str or price_str.lower() == 'free':
        return 0.0
    
    # Remove currency symbols and thousands separators
    price_str = re.sub(r'[^\d.]', '', price_str)
    
    try:
        return float(price_str) if price_str else 0.0
    except (ValueError, TypeError):
        return 0.0

def clean_reviews(reviews: Any) -> int:
    """Clean and convert reviews to integer."""
    if reviews is None:
        return 0
        
    # Handle non-string values
    if not isinstance(reviews, (str, int, float)):
        return 0
    
    # Convert to string if it's a number
    reviews_str = str(reviews).strip()
    
    # Return 0 for empty strings or non-numeric text
    if not reviews_str or not any(c.isdigit() for c in reviews_str):
        return 0
    
    # Extract digits from strings like '128 reviews' or '1.2K reviews'
    match = re.search(r'(\d+(?:\.\d+)?[KkMmBb]?)\s*(?:reviews?|ratings?)?', reviews_str, re.IGNORECASE)
    if match:
        num = match.group(1).lower()
        try:
            if 'k' in num:
                return int(float(num.replace('k', '')) * 1000)
            elif 'm' in num:
                return int(float(num.replace('m', '')) * 1000000)
            elif 'b' in num:
                return int(float(num.replace('b', '')) * 1000000000)
            return int(float(num))
        except (ValueError, TypeError):
            return 0
    
    try:
        return int(float(reviews_str)) if reviews_str else 0
    except (ValueError, TypeError):
        return 0

def clean_rating(rating: Any) -> Optional[float]:
    """Clean and validate rating (0-5 scale)."""
    if rating is None:
        return None
    try:
        rating = float(rating)
        return max(0.0, min(5.0, rating))  # Clamp between 0-5
    except (ValueError, TypeError):
        return None

def clean_category(category: Any) -> str:
    """Clean and standardize category names."""
    if not category:
        return "uncategorized"
    
    category = clean_text(category).lower()
    
    # Map variations to standard category names
    category_mapping = {
        'snacks': ['snack', 'biscuit', 'chips', 'chocolate'],
        'beverages': ['beverage', 'drink', 'juice', 'soda', 'water'],
        'dairies': ['dairy', 'milk', 'cheese', 'yogurt'],
        'personal-care': ['personal care', 'beauty', 'cosmetic', 'skincare', 'haircare'],
        'home-living': ['home', 'living', 'furniture', 'decor'],
        'electronics': ['electronic', 'gadget', 'device'],
        'fashion': ['clothing', 'apparel', 'wear', 'shirt', 'dress', 'jeans'],
        'phones-accessories': ['phone', 'smartphone', 'mobile', 'accessory', 'earphone', 'headphone'],
    }
    
    # Check for matches in category mappings
    for main_cat, keywords in category_mapping.items():
        if any(keyword in category for keyword in keywords):
            return main_cat
    
    return category if category else "uncategorized"

def clean_product_data(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and standardize product data from Jumia.
    
    Args:
        product: Raw product data as a dictionary
        
    Returns:
        Dict containing cleaned product data
    """
    if not isinstance(product, dict):
        return {}
    
    try:
        # Clean basic fields
        name = clean_text(product.get('name'))
        brand = clean_text(product.get('brand'))
        price = clean_price(product.get('price', 0))
        
        # Extract brand from name if not provided
        if not brand and name:
            # Simple heuristic: first word in name is often the brand
            brand = name.split()[0] if name else ""
        
        # Clean and validate other fields
        cleaned = {
            'name': name,
            'brand': brand,
            'price': price,
            'original_price': clean_price(product.get('original_price', price)),
            'discount_pct': min(100, max(0, int(product.get('discount_pct', 0)))),
            'rating': clean_rating(product.get('rating')),
            'reviews': clean_reviews(product.get('reviews')),  # Use the new clean_reviews function
            'in_stock': bool(product.get('in_stock', True)),
            'category': clean_category(product.get('category')),
            'link': clean_text(product.get('link', '')).split('?')[0],  # Remove query params
            'scraped_at': datetime.utcnow().isoformat(),
            'source': 'jumia',
        }
        
        # Calculate discount percentage if not provided but original price is
        if 'original_price' in product and not cleaned['discount_pct'] and cleaned['original_price'] > 0:
            cleaned['discount_pct'] = min(100, int(
                ((cleaned['original_price'] - cleaned['price']) / cleaned['original_price']) * 100
            ))
        
        # Ensure required fields
        if not cleaned['name'] or not cleaned['link']:
            return {}
            
        return cleaned
        
    except Exception as e:
        logger.error(f"Error cleaning product data: {e}\nOriginal data: {json.dumps(product, indent=2)}")
        return {}

def clean_product_batch(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Clean a batch of product data.
    
    Args:
        products: List of raw product dictionaries
        
    Returns:
        List of cleaned product dictionaries
    """
    if not isinstance(products, list):
        return []
    
    cleaned_products = []
    for product in products:
        cleaned = clean_product_data(product)
        if cleaned:  # Only include products that passed validation
            cleaned_products.append(cleaned)
    
    return cleaned_products
