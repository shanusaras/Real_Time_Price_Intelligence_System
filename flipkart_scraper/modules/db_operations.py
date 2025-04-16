from sqlalchemy.orm import Session
import pandas as pd
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ScraperDBManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def save_product_data(self, products_data):
        """
        Save scraped product data to database
        Args:
            products_data: List of dicts containing product and price_history data
        """
        with self.db_manager.get_session() as session:
            for data in products_data:
                try:
                    # Check if product already exists
                    existing_product = session.query(Product).filter(
                        Product.name == data['product']['name'],
                        Product.category == data['product']['category']
                    ).first()

                    if existing_product:
                        # Update existing product
                        for key, value in data['product'].items():
                            if key not in ['id', 'created_at']:
                                setattr(existing_product, key, value)
                        product = existing_product
                    else:
                        # Create new product
                        product = Product(**data['product'])
                        session.add(product)
                        session.flush()  # Get product ID

                    # Add price history
                    price_data = data['price_history']
                    price_data['product_id'] = product.id
                    price_history = PriceHistory(**price_data)
                    session.add(price_history)

                    logger.info(f"Saved/Updated product: {product.name}")

                except Exception as e:
                    logger.error(f"Error saving product {data['product'].get('name')}: {str(e)}")
                    session.rollback()
                    continue

            try:
                session.commit()
                logger.info(f"Successfully saved {len(products_data)} products")
            except Exception as e:
                logger.error(f"Error committing transaction: {str(e)}")
                session.rollback()
                raise
