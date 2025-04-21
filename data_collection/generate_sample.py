import json

with open('data_collection/data/sample_all_products.json', encoding='utf-8') as f:
    data = json.load(f)

def assign_category(rec):
    kws = [k.lower() for k in rec.get('_keywords',[])]
    if 'beverage' in kws: return 'beverages'
    if 'snack'    in kws: return 'snacks'
    # …add your other buckets…
    return 'other'

for rec in data:
    rec['scraped_category'] = assign_category(rec)

sample = data[:100]

with open('data_collection/data/sample_by_category.json','w', encoding='utf-8') as out:
    json.dump(sample, out, indent=2)

print("Wrote sample_by_category.json with", len(sample), "records")