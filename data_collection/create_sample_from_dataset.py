import json
import os

# Path to the existing full dataset
full_data_path = os.path.join(os.path.dirname(__file__), 'data', 'openfoodfacts_products.json')
# Path where the sample will be saved
sample_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_all_products.json')

# Number of sample records to save
SAMPLE_SIZE = 100

if not os.path.exists(full_data_path):
    print(f"Full dataset not found at {full_data_path}.")
    exit(1)

with open(full_data_path, 'r', encoding='utf-8') as f:
    products = json.load(f)

sample_products = products[:SAMPLE_SIZE]

with open(sample_path, 'w', encoding='utf-8') as f:
    json.dump(sample_products, f, indent=2, ensure_ascii=False)

print(f"Sample of {len(sample_products)} products written to: {sample_path}")
