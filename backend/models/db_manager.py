from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pymongo import MongoClient
from contextlib import contextmanager
from config.config import config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize database connections"""
        try:
            # MySQL setup
            self.mysql_engine = create_engine(config.MYSQL_URI)
            self.SessionFactory = sessionmaker(bind=self.mysql_engine)
            self.Session = scoped_session(self.SessionFactory)
            
            # MongoDB setup
            self.mongo_client = MongoClient(config.MONGODB_URI)
            self.mongo_db = self.mongo_client[config.MONGODB_DB]
            
            logger.info("Database connections initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            raise
    
    @contextmanager
    def get_session(self):
        """Get a PostgreSQL session with automatic cleanup"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_mongo_collection(self, collection_name: str):
        """Get a MongoDB collection"""
        return self.mongo_db[collection_name]
    
    def close_connections(self):
        """Close all database connections"""
        try:
            self.Session.remove()
            self.mongo_client.close()
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
            raise

# Create a global instance
db_manager = DatabaseManager()
