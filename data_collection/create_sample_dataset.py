import os
import json

def main():
    base_dir = os.path.dirname(__file__)
    raw_dir = os.path.join(base_dir, 'raw_data')
    sample_dir = os.path.join(base_dir, 'data')
    os.makedirs(sample_dir, exist_ok=True)
    input_path = os.path.join(raw_dir, 'jumia_playwright.json')
    output_path = os.path.join(sample_dir, 'sample_by_category.json')
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    sample = data[:100]
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2)
    print(f"Sample dataset written to {output_path}")

if __name__ == '__main__':
    main()
