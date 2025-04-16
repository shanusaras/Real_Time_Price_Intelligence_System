import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config import config
from database import Base, get_engine, Product, PriceHistory, CompetitorPrice
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_postgresql():
    """Initialize PostgreSQL database"""
    try:
        engine = get_engine(config.POSTGRES_URI)
        Base.metadata.create_all(engine)
        logger.info("PostgreSQL database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating PostgreSQL tables: {e}")
        raise

def init_mongodb():
    """Initialize MongoDB collections"""
    try:
        client = MongoClient(config.MONGODB_URI)
        db = client[config.MONGODB_DB]
        
        # Create collections with validators
        db.create_collection("product_analytics", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["product_id", "timestamp"],
                "properties": {
                    "product_id": {"bsonType": "int"},
                    "timestamp": {"bsonType": "date"},
                    "price_trends": {"bsonType": "object"},
                    "demand_forecast": {"bsonType": "object"},
                    "competitor_analysis": {"bsonType": "object"}
                }
            }
        })
        
        db.create_collection("market_insights", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["category", "timestamp"],
                "properties": {
                    "category": {"bsonType": "string"},
                    "timestamp": {"bsonType": "date"},
                    "market_trends": {"bsonType": "object"},
                    "seasonal_patterns": {"bsonType": "object"}
                }
            }
        })
        
        # Create indexes
        db.product_analytics.create_index([("product_id", 1), ("timestamp", -1)])
        db.market_insights.create_index([("category", 1), ("timestamp", -1)])
        
        logger.info("MongoDB collections and indexes created successfully")
    except Exception as e:
        logger.error(f"Error setting up MongoDB: {e}")
        raise

def main():
    """Initialize all databases"""
    try:
        init_postgresql()
        init_mongodb()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
