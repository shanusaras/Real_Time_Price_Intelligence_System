"""
ETL Data Validation Script

This script provides validation and verification functions for the ETL pipeline.
It's used to ensure data integrity and quality after ETL processes.
"""
from sqlalchemy import func, text
from etl.src.database import SessionLocal, Category, Product, Price

def get_session():
    """Create a new database session."""
    return SessionLocal()

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text}".upper())
    print("=" * 80)

def validate_etl_results():
    """Validate ETL results by checking data integrity and completeness."""
    with get_session() as session:
        # 1. Get basic counts
        total_products = session.query(Product).count()
        total_prices = session.query(Price).count()
        total_categories = session.query(Category).count()
        
        print_header("ETL VALIDATION: BASIC COUNTS")
        print(f"Total Products: {total_products:,}")
        print(f"Total Price Entries: {total_prices:,}")
        print(f"Total Categories: {total_categories}")
        
        # 2. Get category distribution using raw SQL for simplicity
        category_dist = session.execute(text("""
            SELECT c.name, COUNT(p.id) as product_count 
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.name
            ORDER BY product_count DESC
        """)).fetchall()
        
        print_header("ETL VALIDATION: CATEGORY DISTRIBUTION")
        print(f"{'Category':<25} | {'Count':>8}")
        print("-" * 36)
        for name, count in category_dist:
            print(f"{name:<25} | {count:>8,}")
        
        # 3. Check for missing data
        missing_data = session.execute(text("""
            SELECT 
                COUNT(*) as total_products,
                SUM(CASE WHEN p.name IS NULL OR p.name = '' THEN 1 ELSE 0 END) as missing_names,
                SUM(CASE WHEN p.brand IS NULL OR p.brand = '' THEN 1 ELSE 0 END) as missing_brands,
                (SELECT COUNT(DISTINCT p.id) FROM products p 
                 LEFT JOIN prices pr ON p.id = pr.product_id 
                 WHERE pr.id IS NULL) as missing_prices
            FROM products p
        """)).fetchone()
        
        print_header("ETL VALIDATION: DATA COMPLETENESS")
        print(f"Total Products: {missing_data[0]:,}")
        print(f"Products missing names: {missing_data[1]:,} ({(missing_data[1]/missing_data[0]*100):.2f}%)")
        print(f"Products missing brands: {missing_data[2]:,} ({(missing_data[2]/missing_data[0]*100):.2f}%)")
        print(f"Products missing prices: {missing_data[3]:,} ({(missing_data[3]/missing_data[0]*100):.2f}%)")

if __name__ == "__main__":
    try:
        print("\n" + "=" * 60)
        print("  ETL DATA VALIDATION CHECKS")
        print("=" * 60)
        
        validate_etl_results()
        
        print("\n" + "=" * 60)
        print("  VALIDATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR during validation: {str(e)}")
        raise
