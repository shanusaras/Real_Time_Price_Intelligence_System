from typing import Dict, List, Optional, Tuple
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_product(product: Dict) -> Tuple[bool, List[str]]:
    """
    Validate product data
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of error messages)
    """
    errors = []
    
    # Required fields
    if not product.get('name'):
        errors.append("Product name is required")
    elif len(product['name']) > 255:
        errors.append("Product name too long (max 255 chars)")
    
    # Category validation
    if not product.get('category'):
        errors.append("Category is required")
    elif len(product['category']) > 100:
        errors.append("Category name too long (max 100 chars)")
    
    # Brand validation (optional but with constraints)
    if 'brand' in product and product['brand']:
        if len(product['brand']) > 100:
            errors.append("Brand name too long (max 100 chars)")
        if not re.match(r'^[a-zA-Z0-9\s\-&]+$', product['brand']):
            errors.append("Brand contains invalid characters")
    
    # Description validation (optional but with constraints)
    if 'description' in product and product['description']:
        if len(product['description']) > 1000:
            errors.append("Description too long (max 1000 chars)")
    
    # Rating validation (optional but with constraints)
    if 'rating' in product and product['rating'] is not None:
        if not isinstance(product['rating'], (int, float)):
            errors.append("Rating must be a number")
        elif not 0 <= product['rating'] <= 5:
            errors.append("Rating must be between 0 and 5")
    
    # Timestamp validation
    for field in ['created_at', 'updated_at']:
        if field in product:
            if not isinstance(product[field], datetime):
                errors.append(f"{field} must be a datetime object")
    
    return len(errors) == 0, errors

def validate_price_history(price_data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate price history data
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of error messages)
    """
    errors = []
    
    # Price validation (required)
    if 'price' not in price_data:
        errors.append("Price is required")
    elif not isinstance(price_data['price'], (int, float)):
        errors.append("Price must be a number")
    elif price_data['price'] <= 0:
        errors.append("Price must be greater than 0")
    
    # Currency validation (required)
    if not price_data.get('currency'):
        errors.append("Currency is required")
    elif len(price_data['currency']) != 3:
        errors.append("Currency must be a 3-letter code")
    elif not price_data['currency'].isalpha():
        errors.append("Currency must contain only letters")
    
    # Timestamp validation (required)
    if 'timestamp' not in price_data:
        errors.append("Timestamp is required")
    elif not isinstance(price_data['timestamp'], datetime):
        errors.append("Timestamp must be a datetime object")
    
    # URL validation (optional but with constraints)
    if 'url' in price_data and price_data['url']:
        if len(price_data['url']) > 500:
            errors.append("URL too long (max 500 chars)")
        if not price_data['url'].startswith(('http://', 'https://')):
            errors.append("URL must start with http:// or https://")
    
    # Source validation (required)
    if not price_data.get('source'):
        errors.append("Source is required")
    elif len(price_data['source']) > 50:
        errors.append("Source name too long (max 50 chars)")
    
    return len(errors) == 0, errors

def validate_product_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate complete product data including both product and price history
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of error messages)
    """
    if not isinstance(data, dict):
        return False, ["Invalid data format"]
    
    if 'product' not in data or 'price_history' not in data:
        return False, ["Missing product or price_history data"]
    
    # Validate product data
    product_valid, product_errors = validate_product(data['product'])
    
    # Validate price history data
    price_valid, price_errors = validate_price_history(data['price_history'])
    
    # Combine all errors
    all_errors = []
    if not product_valid:
        all_errors.extend([f"Product error: {err}" for err in product_errors])
    if not price_valid:
        all_errors.extend([f"Price error: {err}" for err in price_errors])
    
    return len(all_errors) == 0, all_errors
