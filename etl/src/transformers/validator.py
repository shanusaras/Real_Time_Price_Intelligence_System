"""
Data validation functions for the ETL pipeline.
"""
import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Valid categories based on our standardization
VALID_CATEGORIES = {
    'snacks', 'beverages', 'dairies', 'personal-care', 'home-living',
    'electronics', 'fashion', 'phones-accessories', 'uncategorized'
}

def validate_product_data(product: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate product data against schema and business rules.
    
    Args:
        product: Product data dictionary to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(product, dict):
        return False, "Product data must be a dictionary"
    
    # Required fields check
    required_fields = {
        'name': str,
        'price': (int, float),
        'category': str,
        'link': str,
        'source': str
    }
    
    for field, field_type in required_fields.items():
        if field not in product:
            return False, f"Missing required field: {field}"
        if not isinstance(product[field], field_type):
            return False, f"Field '{field}' must be of type {field_type.__name__}"
        if field != 'price' and not product[field]:
            return False, f"Field '{field}' cannot be empty"
    
    # Price validation
    price = product.get('price')
    if not isinstance(price, (int, float)) or price < 0:
        return False, f"Price must be a positive number, got {price}"
    
    # Original price validation if present
    if 'original_price' in product and product['original_price'] is not None:
        original_price = product['original_price']
        if not isinstance(original_price, (int, float)) or original_price < 0:
            return False, f"Original price must be a positive number, got {original_price}"
        if original_price < price:
            return False, f"Original price ({original_price}) cannot be less than current price ({price})"
    
    # Discount percentage validation
    discount = product.get('discount_pct', 0)
    if not isinstance(discount, (int, float)) or not (0 <= discount <= 100):
        return False, f"Discount percentage must be between 0 and 100, got {discount}"
    
    # Rating validation
    if 'rating' in product and product['rating'] is not None:
        rating = product['rating']
        if not isinstance(rating, (int, float)) or not (0 <= rating <= 5):
            return False, f"Rating must be between 0 and 5, got {rating}"
    
    # Reviews validation
    if 'reviews' in product:
        reviews = product['reviews']
        if not isinstance(reviews, int) or reviews < 0:
            return False, f"Review count must be a non-negative integer, got {reviews}"
    
    # URL validation
    if 'link' in product and product['link']:
        link = product['link']
        if not (link.startswith('http://') or link.startswith('https://')):
            return False, f"Invalid URL: {link}"
    
    # Category validation
    if 'category' in product and product['category']:
        category = product['category']
        if not isinstance(category, str):
            return False, "Category must be a string"
        if len(category) > 100:
            return False, "Category name too long (max 100 characters)"
        if category not in VALID_CATEGORIES:
            logger.warning(f"Category '{category}' not in standard categories")
    
    # Brand validation
    if 'brand' in product and product['brand'] is not None:
        brand = product['brand']
        if not isinstance(brand, str):
            return False, "Brand must be a string"
        if len(brand) > 100:
            return False, "Brand name too long (max 100 characters)"
    
    # Timestamp validation
    if 'scraped_at' in product and product['scraped_at']:
        try:
            datetime.fromisoformat(product['scraped_at'])
        except (ValueError, TypeError) as e:
            return False, f"Invalid timestamp format: {e}"
    
    return True, ""

def validate_product_batch(products: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validate a batch of product data.
    
    Args:
        products: List of product dictionaries to validate
        
    Returns:
        tuple: (all_valid: bool, valid_products: List[Dict], invalid_products: List[Dict])
    """
    if not isinstance(products, list):
        return False, [], []
    
    valid_products = []
    invalid_products = []
    
    for product in products:
        is_valid, message = validate_product_data(product)
        if is_valid:
            valid_products.append(product)
        else:
            logger.warning(f"Invalid product: {message}")
            invalid_products.append({
                'product': product,
                'error': message
            })
    
    all_valid = len(invalid_products) == 0
    if not all_valid:
        logger.warning(f"Found {len(invalid_products)} invalid products out of {len(products)}")
    
    return all_valid, valid_products, invalid_products

def validate_price_history(prices: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Validate price history data.
    
    Args:
        prices: List of price history entries
        
    Returns:
        tuple: (is_valid: bool, List of valid price entries)
    """
    if not isinstance(prices, list):
        return False, []
    
    valid_entries = []
    
    for entry in prices:
        if not isinstance(entry, dict):
            logger.warning("Price history entry is not a dictionary")
            continue
            
        required_fields = ['price', 'timestamp']
        if not all(field in entry for field in required_fields):
            logger.warning(f"Missing required fields in price history entry: {entry}")
            continue
            
        try:
            price = float(entry['price'])
            if price < 0:
                logger.warning(f"Invalid price in history: {price}")
                continue
                
            # Validate timestamp format
            datetime.fromisoformat(entry['timestamp'])
            
            valid_entries.append({
                'price': price,
                'timestamp': entry['timestamp']
            })
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid price history entry: {e}")
            continue
    
    return len(valid_entries) > 0, valid_entries
