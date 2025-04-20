import json
import os
from collections import defaultdict

# Define the mapping from hot business categories to relevant keywords
HOT_CATEGORIES = {
    "snacks": ["snack", "chips", "biscuits", "crackers", "popcorn", "namkeen"],
    "beverages": ["beverage", "drink", "juice", "water", "soda", "soft drink", "energy drink", "tea", "coffee"],
    "dairies": ["dairy", "milk", "cheese", "yogurt", "curd", "paneer", "butter", "cream", "ghee", "lactose-free", "plant-based milk"],
    "personal-care": ["personal care", "soap", "shampoo", "toothpaste", "handwash", "sanitizer", "lotion", "cream", "face wash", "deodorant", "body wash"],
    "dietary-supplements": ["supplement", "vitamin", "protein", "nutrition", "nutritional", "health bar", "multivitamin", "omega", "probiotic", "energy bar"]
}

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'data', 'all_products_openfoodfacts.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'data', 'all_products_by_category.json')

# Load the existing 25,000 products
with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Prepare a dict to hold categorized products
categorized = defaultdict(list)

for prod in products:
    # Try to find a category match using product's 'categories' field or product_name
    prod_categories = prod.get('categories', '').lower()
    prod_name = prod.get('product_name', '').lower()
    matched = False
    for cat, keywords in HOT_CATEGORIES.items():
        for kw in keywords:
            if kw in prod_categories or kw in prod_name:
                categorized[cat].append(prod)
                matched = True
                break
        if matched:
            break
    if not matched:
        # Optionally, you can collect uncategorized products
        pass

# Save categorized products to a new JSON file
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(categorized, f, indent=2, ensure_ascii=False)

print(f"Categorized products saved to: {OUTPUT_PATH}")
for cat in HOT_CATEGORIES:
    print(f"{cat}: {len(categorized[cat])} products")
