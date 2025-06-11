# Data Transformers Module

This module handles the transformation and validation of raw product data into a clean, standardized format suitable for analysis and storage.

## Overview

The transformers module consists of two main components:

1. **Cleaner** (`cleaner.py`): Cleans and normalizes raw product data
2. **Validator** (`validator.py`): Validates the cleaned data against defined rules

## Cleaner Module (`cleaner.py`)

### Core Functions

#### `clean_text(text: Any) -> str`
- **Purpose**: Normalize and clean text data
- **Handles**:
  - `None` values → empty string
  - Non-string values → string conversion
  - Extra whitespace and newlines
  - Leading/trailing spaces

#### `clean_price(price: Any) -> float`
- **Purpose**: Convert various price formats to float
- **Handles**:
  - Currency symbols (₦, $, etc.)
  - Thousands separators (commas, periods)
  - "Free" or empty values → 0.0
  - Non-numeric values → 0.0

#### `clean_reviews(reviews: Any) -> int`
- **Purpose**: Convert review counts to integer
- **Handles**:
  - String formats ("128", "1.2K", "5.5M")
  - Non-numeric values → 0
  - Negative numbers → 0

#### `clean_rating(rating: Any) -> Optional[float]`
- **Purpose**: Normalize rating values (0-5 scale)
- **Handles**:
  - Values outside 0-5 range → clamped to range
  - Non-numeric values → None

#### `clean_category(category: Any) -> str`
- **Purpose**: Standardize category names
- **Mappings**:
  - Maps variations to standard categories (e.g., "electronics" → "electronics")
  - Unknown categories → "uncategorized"

#### `clean_product_data(product: Dict[str, Any]) -> Dict[str, Any]`
- **Purpose**: Clean all fields of a product
- **Features**:
  - Handles missing/optional fields
  - Calculates discount percentages
  - Adds metadata (scraped_at, source)
  - Filters out invalid products (returns empty dict)

#### `clean_product_batch(products: List[Dict]) -> List[Dict]`
- **Purpose**: Clean a batch of products
- **Features**:
  - Processes multiple products efficiently
  - Only includes valid products in output
  - Maintains original product structure

## Validator Module (`validator.py`)

### Core Functions

#### `validate_product_data(product: Dict) -> Tuple[bool, str]`
- **Purpose**: Validate a single product
- **Checks**:
  - Required fields present
  - Field types match expected types
  - Price and discount values are valid
  - URLs are properly formatted
  - Ratings are within valid range
- **Returns**: (is_valid: bool, error_message: str)

#### `validate_product_batch(products: List[Dict]) -> Tuple[bool, List[Dict], List[Dict]]`
- **Purpose**: Validate a batch of products
- **Returns**:
  - all_valid: bool (True if all products are valid)
  - valid_products: List of valid products
  - invalid_products: List of dicts with 'product' and 'error' keys

## Usage Example

```python
from etl.src.transformers.cleaner import clean_product_batch
from etl.src.transformers.validator import validate_product_batch

# Clean raw product data
cleaned_products = clean_product_batch(raw_products)

# Validate cleaned data
all_valid, valid_products, invalid_products = validate_product_batch(cleaned_products)

if not all_valid:
    print(f"Found {len(invalid_products)} invalid products")
    for item in invalid_products:
        print(f"Error: {item['error']}")
        print(f"Product: {item['product']['name']}")
```

## Error Handling

- **Cleaner**: Returns empty dict for invalid products
- **Validator**: Returns detailed error messages for each validation failure
- Both modules include comprehensive logging

## Dependencies

- Python 3.8+
- Standard library only (no external dependencies)

## Testing

Run the test script to see examples of the transformer in action:

```bash
python quick_test.py
```

## Contributing

When adding new cleaning or validation rules:
1. Add tests for new functionality
2. Update this documentation
3. Maintain backward compatibility
