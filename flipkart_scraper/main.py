# main.py — Developer Test Runner (1 Category Only)

from modules.fetcher import get_html
from modules.parser import parse_data
import pandas as pd
import os

# Make sure folders exist (if running independently)
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Test category (change this for debugging)
category = "laptop"

# Fetch HTML (for fewer pages to keep it light)
html = get_html(category, num_pages=2)

# Parse the data
records = parse_data(html, category=category)
print(f"✅ Parsed {len(records)} records for {category}")

# Save sample output
df = pd.DataFrame(records)
df.to_csv(f"data/{category}_sample_test.csv", index=False)
print(f"📁 Saved test data → data/{category}_sample_test.csv")