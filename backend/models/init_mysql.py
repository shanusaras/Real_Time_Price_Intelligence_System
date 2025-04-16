from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config import config
from database import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_mysql():
    """Initialize MySQL database"""
    try:
        # Create database URL
        database_url = config.MYSQL_URI
        
        # Create database if it doesn't exist
        engine = create_engine(database_url)
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"Created database: {config.MYSQL_DB}")
        
        # Create all tables
        Base.metadata.create_all(engine)
        logger.info("Successfully created all tables")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    init_mysql()
