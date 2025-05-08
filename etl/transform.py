
import os
import pandas as pd
from sqlalchemy.orm import Session
from models import Product, PriceHistory, SessionLocal

"""
ETL Transform:
- Reads raw JSON from Jumia scrape
- Cleans and normalizes
- Loads to MySQL using SQLAlchemy models
"""

def main():
    # 1. Extract: Load raw JSON data
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data_collection', 'data', 'jumia_playwright.json')
    if not os.path.exists(raw_path):
        print(f"File not found: {raw_path}")
        return
    df = pd.read_json(raw_path)
    print(f"Loaded {len(df)} records from {raw_path}")

    # 2. Transform: Clean and normalize data
    df = df.drop_duplicates(subset=["name", "brand", "category"])  # Remove duplicates
    df = df.fillna({
        "brand": "Unknown",
        "discount_pct": 0,
        "rating": 0,
        "reviews": 0,
        "in_stock": True
    })
    # Ensure correct data types
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce").fillna(0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
    df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce").fillna(0)

    # 3. Load: Insert into MySQL using SQLAlchemy models
    session = SessionLocal()
    products_added = 0
    prices_added = 0
    try:
        for _, row in df.iterrows():
            # Check if product already exists
            product = session.query(Product).filter_by(
                name=row["name"], brand=row["brand"], category=row["category"]
            ).first()
            if not product:
                product = Product(
                    name=row["name"],
                    brand=row["brand"],
                    category=row["category"],
                    link=row.get("link", None)
                )
                session.add(product)
                session.flush()  # Assign product_id
                products_added += 1
            # Add price history
            price_hist = PriceHistory(
                product_id=product.product_id,
                price=row["price"],
                discount_pct=row["discount_pct"],
                in_stock=bool(row["in_stock"]),
                rating=row["rating"],
                reviews=int(row["reviews"])
            )
            session.add(price_hist)
            prices_added += 1
        session.commit()
        print(f"Inserted {products_added} new products and {prices_added} price records into MySQL.")
    except Exception as e:
        print("Error during ETL:", e)
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    main()

    # Load raw Jumia JSON
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data_collection', 'data', 'jumia_playwright.json')
    df = pd.read_json(raw_path)
    print(f"Loaded {len(df)} records from Jumia JSON.")

    # TODO: Data cleaning (e.g., drop duplicates, fill NAs)

    # Example: Export to CSV for analysis
    out_csv = os.path.join(os.path.dirname(__file__), 'output', 'jumia_products_clean.csv')
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"Clean data exported to {out_csv}")

if __name__ == '__main__':
    main()
