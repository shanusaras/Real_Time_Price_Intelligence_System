import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
df = pd.read_csv('etl/output/jumia_products_clean.csv')

# Basic statistics
print("\n=== Basic Statistics ===")
print(f"Total number of records: {len(df)}")
print(f"Number of unique categories: {df['category'].nunique()}")
print(f"Number of unique brands: {df['brand'].nunique()}")

# Price statistics
print("\n=== Price Statistics ===")
print(df['price'].describe())

# Category distribution
print("\n=== Category Distribution ===")
category_dist = df['category'].value_counts()
print(category_dist)

# Price distribution by category
print("\n=== Average Price by Category ===")
avg_price_by_cat = df.groupby('category')['price'].mean().sort_values(ascending=False)
print(avg_price_by_cat)

# Rating distribution
print("\n=== Rating Distribution ===")
print(df['rating'].describe())

# Reviews distribution
print("\n=== Reviews Distribution ===")
print(df['reviews'].describe())

# In stock status
print("\n=== In Stock Status ===")
print(df['in_stock'].value_counts())

# Create visualizations
plt.figure(figsize=(12, 6))

# Price distribution
plt.subplot(2, 2, 1)
sns.histplot(df['price'], bins=50)
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.yscale('log')  # Use log scale for better visualization

# Category distribution
plt.subplot(2, 2, 2)
category_dist.plot(kind='bar')
plt.title('Category Distribution')
plt.xlabel('Category')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)

# Price by category
plt.subplot(2, 2, 3)
sns.boxplot(x='category', y='price', data=df)
plt.title('Price Distribution by Category')
plt.xticks(rotation=45)
plt.yscale('log')

# Rating distribution
plt.subplot(2, 2, 4)
sns.histplot(df['rating'], bins=10)
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('etl/output/data_analysis_visualizations.png')
plt.close()

# Save summary statistics to a file
with open('etl/output/data_analysis_summary.txt', 'w') as f:
    f.write("=== Basic Statistics ===\n")
    f.write(f"Total number of records: {len(df)}\n")
    f.write(f"Number of unique categories: {df['category'].nunique()}\n")
    f.write(f"Number of unique brands: {df['brand'].nunique()}\n\n")
    
    f.write("=== Price Statistics ===\n")
    f.write(str(df['price'].describe()) + "\n\n")
    
    f.write("=== Category Distribution ===\n")
    f.write(str(category_dist) + "\n\n")
    
    f.write("=== Average Price by Category ===\n")
    f.write(str(avg_price_by_cat) + "\n\n")
    
    f.write("=== Rating Distribution ===\n")
    f.write(str(df['rating'].describe()) + "\n\n")
    
    f.write("=== Reviews Distribution ===\n")
    f.write(str(df['reviews'].describe()) + "\n\n")
    
    f.write("=== In Stock Status ===\n")
    f.write(str(df['in_stock'].value_counts()) + "\n")

print("\nAnalysis complete. Check etl/output/data_analysis_summary.txt for detailed statistics.")
