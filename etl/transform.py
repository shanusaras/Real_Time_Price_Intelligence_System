
import os
import sys
import pandas as pd
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import logging
from datetime import datetime
import traceback
import time
import json
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from etl.models import Product, PriceHistory, SessionLocal, ValidationError

# Monitoring Configuration
MONITORING_DIR = Path(os.path.dirname(__file__)) / 'monitoring'
MONITORING_DIR.mkdir(exist_ok=True)

# Alert thresholds
ALERT_THRESHOLDS = {
    'processing_time': 60,  # Alert if processing takes more than 60 seconds
    'null_values': 0.05,    # Alert if more than 5% null values
    'price_range': {
        'min': 0,
        'max': 1000000
    }
}

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'etl.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

"""
ETL Transform:
- Reads raw JSON from Jumia scrape
- Cleans and normalizes
- Loads to MySQL using SQLAlchemy models
- Implements batch processing and error handling
"""

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the data:
    1. Handle missing values
    2. Fix data types
    3. Remove outliers
    4. Standardize categories
    
    Args:
        df: Input DataFrame containing raw data
    
    Returns:
        Cleaned DataFrame with validated data
    
    Raises:
        ValueError: If data cleaning fails
    """
    try:
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=["name", "brand", "category"])
        logger.info(f"Removed duplicates: {initial_count - len(df)} records")
        
        # Handle missing values
        df["brand"] = df["brand"].fillna("Unknown")
        df["discount_pct"] = df["discount_pct"].fillna(0)
        df["rating"] = df["rating"].fillna(0)
        df["reviews"] = df["reviews"].fillna(0)
        df["in_stock"] = df["in_stock"].fillna(True)
        
        # Convert to proper data types
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce")
        df["in_stock"] = df["in_stock"].astype(bool)
        
        # Validate price ranges
        df = df[(df["price"] > 0) & (df["price"] <= 1000000)]
        logger.info(f"Filtered price range: {len(df)} records remaining")
        
        # Standardize categories
        df["category"] = df["category"].str.lower()
        df["category"] = df["category"].str.strip()
        
        # Validate rating (0-5)
        df["rating"] = df["rating"].clip(0, 5)
        
        # Validate reviews (must be non-negative)
        df["reviews"] = df["reviews"].clip(lower=0)
        
        # Validate discount percentage (0-100)
        df["discount_pct"] = df["discount_pct"].clip(0, 100)
        
        # Final validation
        if df.isnull().any().any():
            raise ValueError("Data contains null values after cleaning")
            
        return df
        
    except Exception as e:
        logger.error(f"Data cleaning failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"Data cleaning failed: {str(e)}")

def process_batch(session: Session, df: pd.DataFrame, batch_size: int = 1000) -> tuple[int, int]:
    """
    Process a batch of records and insert into database
    
    Args:
        session: SQLAlchemy session
        df: DataFrame containing data
        batch_size: Size of each batch to process
        
    Returns:
        Tuple of (products_added, prices_added)
    """
    products_added = 0
    prices_added = 0
    
    try:
        # Start transaction
        session.begin()
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            
            # Process products
            for _, row in batch.iterrows():
                try:
                    # Check if product exists
                    existing_product = session.query(Product).filter_by(
                        name=row['name'],
                        brand=row['brand'],
                        category=row['category']
                    ).first()
                    
                    if not existing_product:
                        # Create new product
                        product = Product(
                            name=row['name'],
                            brand=row['brand'],
                            category=row['category'],
                            link=row['link']
                        )
                        session.add(product)
                        products_added += 1
                        
                    # Create price history
                    price_history = PriceHistory(
                        product_id=existing_product.product_id if existing_product else None,
                        price=row['price'],
                        discount_pct=row['discount_pct'],
                        in_stock=row['in_stock'],
                        rating=row['rating'],
                        reviews=row['reviews']
                    )
                    session.add(price_history)
                    prices_added += 1
                    
                except Exception as e:
                    logger.error(f"Failed to process record: {str(e)}")
                    logger.error(traceback.format_exc())
                    continue
            
            # Commit batch
            session.commit()
            logger.info(f"Processed batch {i // batch_size + 1}: {len(batch)} records")
            
        return products_added, prices_added
        
    except Exception as e:
        session.rollback()
        logger.error(f"Batch processing failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise
    finally:
        session.close()

def get_data_quality_metrics(df: pd.DataFrame, start_time: float) -> dict:
    """Calculate data quality metrics"""
    # Ensure category_distribution values are standard Python integers
    category_dist = df['category'].value_counts().to_dict()
    for category, count in category_dist.items():
        category_dist[category] = int(count)

    return {
        'total_records': int(len(df)),
        'null_values': {
            'count': int(df.isnull().sum().sum()),
            'percentage': float((df.isnull().sum().sum() / df.size) * 100 if df.size > 0 else 0)
        },
        'price_statistics': {
            'min': float(df['price'].min()) if not df['price'].empty else 0.0,
            'max': float(df['price'].max()) if not df['price'].empty else 0.0,
            'mean': float(df['price'].mean()) if not df['price'].empty else 0.0,
            'std_dev': float(df['price'].std()) if not df['price'].empty else 0.0
        },
        'category_distribution': category_dist,
        'processing_time': float(time.time() - start_time)
    }

def write_metrics(metrics: dict):
    """Write metrics to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    metrics_file = MONITORING_DIR / f'metrics_{timestamp}.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics written to {metrics_file}")

def check_alerts(metrics: dict):
    """Check for any alerts based on thresholds"""
    alerts = []
    
    # Check processing time
    if metrics['processing_time'] > ALERT_THRESHOLDS['processing_time']:
        alerts.append(f"Processing time alert: {metrics['processing_time']}s > {ALERT_THRESHOLDS['processing_time']}s")
    
    # Check null values
    if metrics['null_values']['percentage'] > ALERT_THRESHOLDS['null_values']:
        alerts.append(f"Null values alert: {metrics['null_values']['percentage']}% > {ALERT_THRESHOLDS['null_values']}%")
    
    # Check price range
    if metrics['price_statistics']['min'] < ALERT_THRESHOLDS['price_range']['min']:
        alerts.append(f"Price range alert: Min price {metrics['price_statistics']['min']} < {ALERT_THRESHOLDS['price_range']['min']}")
    if metrics['price_statistics']['max'] > ALERT_THRESHOLDS['price_range']['max']:
        alerts.append(f"Price range alert: Max price {metrics['price_statistics']['max']} > {ALERT_THRESHOLDS['price_range']['max']}")
    
    if alerts:
        logger.warning("ALERTS DETECTED:")
        for alert in alerts:
            logger.warning(alert)

def main():
    """
    Main ETL process with monitoring and alerts:
    1. Loads clean data
    2. Saves to database
    3. Generates metrics
    4. Checks for alerts
    """
    start_time = time.time()
    
    try:
        # Load clean data
        logger.info("Loading clean data...")
        df = load_raw_data()
        
        # Save to database
        logger.info("Saving to database...")
        save_to_database(df)
        
        # Generate metrics
        metrics = get_data_quality_metrics(df, start_time)
        write_metrics(metrics)
        check_alerts(metrics)
        
        logger.info("ETL process completed successfully!")
        logger.info(f"Total processing time: {metrics['processing_time']:.2f} seconds")
        logger.info(f"Total records processed: {metrics['total_records']}")
        logger.info(f"Null values: {metrics['null_values']['percentage']:.2f}%")
        
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise


def load_raw_data() -> pd.DataFrame:
    """Load clean data from existing CSV file"""
    raw_path = os.path.join(os.path.dirname(__file__), 'output', 'jumia_products_clean.csv')
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Clean data file not found at {raw_path}")
        
    logger.info(f"Loading clean data from {raw_path}")
    df = pd.read_csv(raw_path)
    logger.info(f"Loaded {len(df)} records")
    return df


# This function is no longer needed since we're using pre-cleaned data
# def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:


def save_to_database(df: pd.DataFrame):
    """Save cleaned data to database"""
    try:
        # Save to database
        session = SessionLocal()
        products_added, prices_added = process_batch(session, df)
        
        logger.info(f"Saved {products_added} products")
        logger.info(f"Saved {prices_added} price records")
        
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")
        raise

if __name__ == '__main__':
    main()
