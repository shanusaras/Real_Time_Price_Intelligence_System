"""
ETL Pipeline for processing product data into the database.
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Product, Price, Category
from .transformers.cleaner import clean_product_batch
from .transformers.validator import validate_product_batch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self, input_file: str):
        """Initialize the ETL pipeline with input file."""
        self.input_file = Path(input_file)
        self.session = SessionLocal()
        
    def extract(self) -> List[Dict[str, Any]]:
        """Extract data from the input JSON file."""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise
    
    def transform(self, raw_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Transform raw data using the transformers module.
        
        Returns:
            Tuple of (valid_products, invalid_products)
        """
        if not raw_data:
            logger.warning("No data to transform")
            return [], []
            
        logger.info(f"Starting transformation of {len(raw_data)} items")
        
        # Clean the data
        cleaned_data = clean_product_batch(raw_data)
        logger.info(f"Cleaned {len(cleaned_data)} items")
        
        if not cleaned_data:
            logger.warning("No valid data after cleaning")
            return [], []
        
        # Validate the cleaned data
        is_valid, valid_products, invalid_products = validate_product_batch(cleaned_data)
        
        # Add timestamp to valid products
        timestamp = datetime.utcnow()
        for product in valid_products:
            product['timestamp'] = timestamp
        
        # Log validation results
        logger.info(f"Validation results: {len(valid_products)} valid, {len(invalid_products)} invalid items")
        
        if invalid_products:
            for item in invalid_products[:5]:  # Log first 5 invalid items
                logger.warning(f"Invalid item: {item['error']} - {item['product'].get('name', 'No name')}")
            if len(invalid_products) > 5:
                logger.warning(f"... and {len(invalid_products) - 5} more invalid items")
        
        return valid_products, invalid_products
    
    def _get_or_create_category(self, category_name: str) -> Category:
        """Get or create a category."""
        category = self.session.query(Category).filter(
            Category.name == category_name
        ).first()
        
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.flush()  # Flush to get the ID without committing
            
        return category
    
    def _get_or_create_product(self, item: Dict[str, Any], category_id: int) -> Product:
        """Get or create a product."""
        product = self.session.query(Product).filter(
            Product.link == item['link']
        ).first()
        
        if not product:
            product = Product(
                name=item['name'][:500],  # Ensure we don't exceed column size
                brand=item.get('brand')[:100] if item.get('brand') else None,
                category_id=category_id,
                link=item['link'][:500]  # Ensure we don't exceed column size
            )
            self.session.add(product)
            self.session.flush()
            
        return product
    
    def load(self, transformed_data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        Load transformed data into the database.
        
        Returns:
            Tuple of (products_processed, errors)
        """
        if not transformed_data:
            logger.warning("No data to load")
            return 0, 0
            
        success_count = 0
        error_count = 0
        batch_size = 50  # Process in batches for better performance
        
        try:
            for i in range(0, len(transformed_data), batch_size):
                batch = transformed_data[i:i + batch_size]
                
                try:
                    # Process batch
                    for item in batch:
                        try:
                            # Get or create category
                            category = self._get_or_create_category(
                                item.get('category', 'uncategorized')
                            )
                            
                            # Get or create product
                            product = self._get_or_create_product(item, category.id)
                            
                            # Create price record
                            price = Price(
                                product_id=product.id,
                                price=item['price'],
                                discount_pct=item.get('discount_pct', 0),
                                in_stock=item.get('in_stock', True),
                                rating=item.get('rating'),
                                reviews_count=item.get('reviews_count', 0),
                                timestamp=item['timestamp']
                            )
                            self.session.add(price)
                            success_count += 1
                            
                        except Exception as e:
                            error_count += 1
                            logger.error(f"Error processing item: {e}")
                            logger.debug(f"Item data: {item}")
                            continue
                    
                    # Commit after each batch
                    self.session.commit()
                    
                except Exception as e:
                    self.session.rollback()
                    logger.error(f"Batch failed: {e}")
                    error_count += len(batch)  # Count all items in failed batch
            
            logger.info(f"Successfully loaded {success_count} records with {error_count} errors")
            return success_count, error_count
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Fatal error in load: {e}")
            raise
        finally:
            self.session.close()
    
    def run(self) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline.
        
        Returns:
            Dict containing processing statistics
        """
        stats = {
            'start_time': datetime.utcnow(),
            'extracted': 0,
            'cleaned': 0,
            'valid': 0,
            'invalid': 0,
            'loaded': 0,
            'errors': 0,
            'end_time': None,
            'duration_seconds': None,
            'status': 'failed'
        }
        
        try:
            logger.info("Starting ETL pipeline")
            
            # Extract
            logger.info("Extracting data...")
            raw_data = self.extract()
            stats['extracted'] = len(raw_data)
            logger.info(f"Extracted {stats['extracted']} records")
            
            if not raw_data:
                raise ValueError("No data extracted from source")
            
            # Transform
            logger.info("Transforming data...")
            valid_products, invalid_products = self.transform(raw_data)
            stats['valid'] = len(valid_products)
            stats['invalid'] = len(invalid_products)
            stats['cleaned'] = len(valid_products) + len(invalid_products)
            
            logger.info(f"Transformed {stats['cleaned']} records ({stats['valid']} valid, {stats['invalid']} invalid)")
            
            # Load
            if valid_products:
                logger.info("Loading valid data to database...")
                loaded, errors = self.load(valid_products)
                stats['loaded'] = loaded
                stats['errors'] = errors
                logger.info(f"Loaded {loaded} records with {errors} errors")
            else:
                logger.warning("No valid data to load")
            
            # Update stats
            stats['status'] = 'completed' if stats['loaded'] > 0 else 'completed_with_errors'
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            stats['status'] = 'failed'
            stats['error'] = str(e)
            raise
            
        finally:
            # Finalize stats
            stats['end_time'] = datetime.utcnow()
            stats['duration_seconds'] = (stats['end_time'] - stats['start_time']).total_seconds()
            
            # Log final stats
            logger.info("=" * 50)
            logger.info("ETL Pipeline Summary:")
            logger.info(f"Status: {stats['status'].upper()}")
            logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
            logger.info(f"Extracted: {stats['extracted']}")
            logger.info(f"Cleaned: {stats['cleaned']}")
            logger.info(f"Valid: {stats['valid']}")
            logger.info(f"Invalid: {stats['invalid']}")
            logger.info(f"Loaded: {stats['loaded']}")
            logger.info(f"Errors: {stats['errors']}")
            logger.info("=" * 50)
            
            return stats

def main():
    import argparse
    import json
    import os
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Run ETL pipeline for product data')
    parser.add_argument('input_file', type=str, help='Path to input JSON file')
    parser.add_argument('--output-dir', type=str, default='etl/output', 
                       help='Directory to save output files')
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Initialize and run pipeline
        pipeline = ETLPipeline(args.input_file)
        stats = pipeline.run()
        
        # Save stats to a JSON file
        timestamp = stats['start_time'].strftime('%Y%m%d_%H%M%S')
        stats_file = Path(args.output_dir) / f'etl_stats_{timestamp}.json'
        
        # Convert datetime objects to string for JSON serialization
        serializable_stats = {}
        for key, value in stats.items():
            if hasattr(value, 'isoformat'):  # For datetime objects
                serializable_stats[key] = value.isoformat()
            else:
                serializable_stats[key] = value
        
        with open(stats_file, 'w') as f:
            json.dump(serializable_stats, f, indent=2)
        
        print(f"\nETL Pipeline completed with status: {stats['status'].upper()}")
        print(f"- Duration: {stats['duration_seconds']:.2f} seconds")
        print(f"- Extracted: {stats['extracted']}")
        print(f"- Cleaned: {stats['cleaned']}")
        print(f"- Valid: {stats['valid']}")
        print(f"- Invalid: {stats['invalid']}")
        print(f"- Loaded: {stats['loaded']}")
        print(f"- Errors: {stats['errors']}")
        print(f"\nDetailed stats saved to: {stats_file}")
        
        # Return non-zero exit code if there were errors
        if stats['status'] == 'failed' or stats['errors'] > 0:
            return 1
            
        return 0
        
    except Exception as e:
        print(f"\nETL Pipeline failed: {e}")
        return 1

if __name__ == "__main__":
    main()
