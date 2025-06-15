"""
Database initialization script.

This module handles database initialization and schema creation.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from sqlalchemy import text, inspect, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

from ..models.base import Base
from .session import engine, async_engine, SessionLocal
from ..config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def table_exists(table_name: str, session: Session) -> bool:
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def create_tables(drop_existing: bool = False) -> None:
    """
    Create all database tables defined in SQLAlchemy models.
    
    Args:
        drop_existing: If True, drop existing tables before creating new ones.
    """
    try:
        if drop_existing:
            logger.warning("Dropping all existing tables...")
            Base.metadata.drop_all(bind=engine)
            logger.info("Dropped all existing tables")
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created database tables")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def check_database_connection() -> bool:
    """
    Check if the database connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            session.commit()
        logger.info("Database connection successful")
        return True
    except (SQLAlchemyError, OperationalError) as e:
        logger.error(f"Database connection failed: {e}")
        return False

def get_database_schema() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get the current database schema.
    
    Returns:
        Dict containing table names and their columns
    """
    inspector = inspect(engine)
    schema = {}
    
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                'name': column['name'],
                'type': str(column['type']),
                'nullable': column['nullable'],
                'default': column.get('default'),
                'primary_key': column.get('primary_key', 0) > 0
            })
        schema[table_name] = columns
    
    return schema

def init_database(drop_existing: bool = False) -> None:
    """
    Initialize the database with required tables and data.
    
    Args:
        drop_existing: If True, drop existing tables before creating new ones.
    """
    logger.info("Initializing database...")
    
    if not check_database_connection():
        raise RuntimeError("Failed to connect to the database")
    
    # Create all tables
    create_tables(drop_existing=drop_existing)
    
    # Log the database schema
    schema = get_database_schema()
    logger.info(f"Database schema: {list(schema.keys())}")
    
    logger.info("Database initialization complete")

if __name__ == "__main__":
    import argparse
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Initialize the database")
    parser.add_argument(
        "--drop-existing", 
        action="store_true", 
        help="Drop existing tables before creating new ones"
    )
    parser.add_argument(
        "--log-level", 
        default=settings.LOG_LEVEL,
        help="Set the logging level"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=args.log_level,
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("db_init.log")
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Starting database initialization (drop_existing={args.drop_existing})")
        init_database(drop_existing=args.drop_existing)
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.exception("Failed to initialize database")
        sys.exit(1)
