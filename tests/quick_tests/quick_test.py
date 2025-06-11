print("=== Testing Product Cleaner & Validator ===\n")

# Sample product data
test_products = [
    # Valid product with discount
    {
        'name': 'Wireless Earbuds Pro',
        'price': '₦15,999',
        'original_price': '₦19,999',  # 20% discount
        'link': 'https://example.com/earbuds-pro',
        'rating': '4.5',
        'reviews': '128',
        'in_stock': 'yes'
    },
    # Valid product without discount
    {
        'name': 'Smart Watch',
        'price': '24,500',
        'link': 'https://example.com/watch',
        'rating': '3.8',
        'reviews': '42',
        'in_stock': 'in stock'
    },
    # Invalid product (missing required fields)
    {
        'name': '',  # Missing name
        'price': 'free',  # Invalid price
        'link': 'not-a-url'  # Invalid URL
    },
    # Invalid product (negative price)
    {
        'name': 'Broken Phone',
        'price': '-5000',
        'original_price': '10000',
        'link': 'https://example.com/broken-phone'
    },
    # Edge case testing
    {
        'name': 'Test Edge Cases',
        'price': 'Free',  # Will be set to 0
        'original_price': '100% off',  # Will be removed
        'link': 'https://example.com/edge-case',
        'rating': 'five stars',  # Will be set to None
        'reviews': 'many'  # Will be set to 0
    }
]

print("1. Importing modules...")
import json
from etl.src.transformers.cleaner import clean_product_data, clean_product_batch
from etl.src.transformers.validator import validate_product_batch

print("2. Cleaning the products...")
cleaned_products = []
for i, product in enumerate(test_products, 1):
    try:
        cleaned = clean_product_data(product)
        if cleaned:
            cleaned_products.append(cleaned)
    except Exception as e:
        print(f"\n❌ Error cleaning product {i}:")
        print(f"Error: {e}")
        print("Product data:", json.dumps(product, indent=2))

print("\n3. Validating the cleaned products...")
is_valid, valid_products, invalid_products = validate_product_batch(cleaned_products)

print("\n4. Results:")
print("=" * 60)

# Show valid products
print(f"\n✅ VALID PRODUCTS ({len(valid_products)}):")
print("-" * 60)
for i, product in enumerate(valid_products, 1):
    print(f"\nProduct {i}:")
    print(f"  Name: {product['name']}")
    print(f"  Price: ₦{product['price']:,.2f}")
    if product.get('original_price'):
        print(f"  Original: ₦{product['original_price']:,.2f}")
        print(f"  Discount: {product.get('discount_pct', 0)}%")
    print(f"  Rating: {product.get('rating', 'N/A')} ({product.get('reviews', 0)} reviews)")
    print(f"  Link: {product['link']}")
    print("-" * 40)

# Show cleaning errors (products that failed cleaning)
cleaning_errors = len(test_products) - len(cleaned_products)
if cleaning_errors > 0:
    print(f"\n❌ CLEANING ERRORS ({cleaning_errors}):")
    print("-" * 60)
    for i, product in enumerate(test_products, 1):
        try:
            cleaned = clean_product_data(product)
            if not cleaned:
                print(f"\nProduct {i} was filtered out during cleaning:")
                print(json.dumps(product, indent=2))
        except Exception as e:
            print(f"\nProduct {i} raised an exception during cleaning:")
            print(f"Error: {e}")
            print("Product data:", json.dumps(product, indent=2))

# Show validation errors
if invalid_products:
    print(f"\n❌ INVALID PRODUCTS ({len(invalid_products)}):")
    print("-" * 60)
    for i, item in enumerate(invalid_products, 1):
        print(f"\nProduct {i}:")
        print(f"  Error: {item['error']}")
        print("  Data:")
        for k, v in item['product'].items():
            print(f"    {k}: {v}")
        print("-" * 40)

# Summary
print("\n" + "=" * 60)
print(f"SUMMARY:")
print(f"- Total products processed: {len(test_products)}")
print(f"- Successfully cleaned: {len(cleaned_products)}/{len(test_products)}")
print(f"- Valid products: {len(valid_products)}")
print(f"- Invalid products: {len(invalid_products)}")
print("=" * 60)

print("\nTest complete! 🎉")
