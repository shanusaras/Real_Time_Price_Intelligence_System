import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from config.config import config
from backend.models.database import get_engine, Product, PriceHistory, CompetitorPrice
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sample_data():
    """Load sample product and price data"""
    try:
        # Create database engine and session
        engine = get_engine(config.POSTGRES_URI)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Sample product categories
        categories = ["Electronics", "Home & Kitchen", "Fashion", "Books", "Sports"]
        brands = ["TechPro", "HomeStyle", "FashionX", "BookWorld", "SportMaster"]
        
        # Generate sample products
        products = []
        for i in range(100):  # Create 100 sample products
            category = np.random.choice(categories)
            brand = np.random.choice(brands)
            product = Product(
                name=f"{brand} Product {i+1}",
                category=category,
                brand=brand,
                description=f"Sample description for {brand} product {i+1} in category {category}"
            )
            products.append(product)
        
        # Bulk insert products
        session.bulk_save_objects(products)
        session.commit()
        logger.info(f"Inserted {len(products)} sample products")
        
        # Generate price history
        price_histories = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 1 year of history
        
        for product in products:
            base_price = np.random.uniform(10, 1000)  # Random base price between 10 and 1000
            current_date = start_date
            
            while current_date <= end_date:
                # Add some random price variations
                price_variation = np.random.uniform(-0.1, 0.1)  # ±10% variation
                price = base_price * (1 + price_variation)
                
                price_history = PriceHistory(
                    product_id=product.id,
                    price=round(price, 2),
                    currency="USD",
                    timestamp=current_date,
                    source="sample_data"
                )
                price_histories.append(price_history)
                
                # Generate competitor prices
                for competitor in ["Competitor A", "Competitor B"]:
                    competitor_variation = np.random.uniform(-0.15, 0.15)  # ±15% variation
                    competitor_price = price * (1 + competitor_variation)
                    
                    competitor_price_entry = CompetitorPrice(
                        product_id=product.id,
                        competitor_name=competitor,
                        price=round(competitor_price, 2),
                        currency="USD",
                        timestamp=current_date,
                        url=f"https://example.com/{competitor.lower().replace(' ', '')}/product/{product.id}"
                    )
                    price_histories.append(competitor_price_entry)
                
                current_date += timedelta(days=7)  # Weekly price updates
        
        # Bulk insert price histories
        session.bulk_save_objects(price_histories)
        session.commit()
        logger.info(f"Inserted {len(price_histories)} price history records")
        
    except Exception as e:
        logger.error(f"Error loading sample data: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def main():
    """Main function to load sample data"""
    try:
        load_sample_data()
        logger.info("Sample data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
