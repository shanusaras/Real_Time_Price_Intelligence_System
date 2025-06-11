"""Test the cleaner and validator with sample data."""
import json
from pathlib import Path

# Sample data that matches our expected format
SAMPLE_PRODUCT = {
    'name': 'Test Product',
    'brand': 'Test Brand',
    'price': 100.0,
    'original_price': 120.0,
    'discount_pct': 17,
    'rating': 4.5,
    'reviews': 10,
    'in_stock': True,
    'category': 'electronics',
    'link': 'https://example.com/product',
    'source': 'test',
    'scraped_at': '2025-01-01T12:00:00'
}

def test_cleaner():
    """Test the cleaner functions."""
    from src.transformers.cleaner import clean_product_data
    
    # Test with valid data
    cleaned = clean_product_data(SAMPLE_PRODUCT)
    print("\n=== Cleaned Product ===")
    print(json.dumps(cleaned, indent=2))
    
    # Test with missing required fields
    invalid = {'name': '', 'price': -1}
    cleaned = clean_product_data(invalid)
    print("\n=== Invalid Product (should be empty) ===")
    print(cleaned)

def test_validator():
    """Test the validator functions."""
    from src.transformers.validator import validate_product_data
    
    # Test with valid data
    is_valid, msg = validate_product_data(SAMPLE_PRODUCT)
    print("\n=== Validation Test ===")
    print(f"Valid: {is_valid}, Message: {msg}")
    
    # Test with invalid data
    invalid_product = SAMPLE_PRODUCT.copy()
    invalid_product['price'] = -10
    is_valid, msg = validate_product_data(invalid_product)
    print(f"\nInvalid Price Test - Valid: {is_valid}, Message: {msg}")

if __name__ == "__main__":
    print("=== Testing Cleaner ===")
    test_cleaner()
    
    print("\n=== Testing Validator ===")
    test_validator()
