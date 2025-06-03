from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, DECIMAL, func, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .config import DB_CONFIG
from urllib.parse import quote_plus
from typing import Optional, List
import os
from datetime import datetime

import os
from typing import Optional, List
from datetime import datetime

# Build the MySQL connection URL with URL-encoded password
password = quote_plus(DB_CONFIG['password'])
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{password}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ValidationError(Exception):
    """Custom validation error for data validation failures"""
    pass

class Product(Base):
    """Represents a product in the database"""
    
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    brand = Column(String(100))
    category = Column(String(100), nullable=False)  # Made category required
    link = Column(Text, nullable=False)  # Made link required
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    price_history = relationship('PriceHistory', back_populates='product', cascade="all, delete-orphan")
    
    @staticmethod
    def validate_data(data: dict) -> None:
        """Validate product data before insertion"""
        if not data.get('name'):
            raise ValidationError("Product name is required")
        if not data.get('category'):
            raise ValidationError("Product category is required")
        if not data.get('link'):
            raise ValidationError("Product link is required")
        
        # Validate category format
        if not isinstance(data['category'], str):
            raise ValidationError("Category must be a string")
        
        # Validate name length
        if len(data['name']) > 1000:
            raise ValidationError("Product name is too long")
        
        # Validate link format
        if not isinstance(data['link'], str):
            raise ValidationError("Link must be a string")
        if not data['link'].startswith(('http://', 'https://')):
            raise ValidationError("Invalid link format")

class PriceHistory(Base):
    """Represents price history for a product"""
    
    __tablename__ = 'price_history'
    
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    discount_pct = Column(DECIMAL(5, 2), default=0)
    in_stock = Column(Boolean, default=True)
    rating = Column(Float, CheckConstraint('rating >= 0 AND rating <= 5'))
    reviews = Column(Integer, default=0)
    scraped_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product = relationship('Product', back_populates='price_history')
    
    @staticmethod
    def validate_data(data: dict) -> None:
        """Validate price history data before insertion"""
        if data.get('price') is None:
            raise ValidationError("Price is required")
            
        # Validate price
        if not isinstance(data['price'], (int, float)):
            raise ValidationError("Price must be a number")
        if data['price'] < 0 or data['price'] > 1000000:
            raise ValidationError("Price must be between 0 and 1000000")
            
        # Validate discount percentage
        if data.get('discount_pct') is not None:
            if not isinstance(data['discount_pct'], (int, float)):
                raise ValidationError("Discount percentage must be a number")
            if data['discount_pct'] < 0 or data['discount_pct'] > 100:
                raise ValidationError("Discount percentage must be between 0 and 100")
                
        # Validate rating
        if data.get('rating') is not None:
            if not isinstance(data['rating'], (int, float)):
                raise ValidationError("Rating must be a number")
            if data['rating'] < 0 or data['rating'] > 5:
                raise ValidationError("Rating must be between 0 and 5")
                
        # Validate reviews
        if data.get('reviews') is not None:
            if not isinstance(data['reviews'], int):
                raise ValidationError("Reviews must be an integer")
            if data['reviews'] < 0:
                raise ValidationError("Reviews cannot be negative")

# Create tables if they don't exist
def create_tables():
    """Create database tables if they don't exist"""
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        raise Exception(f"Failed to create tables: {str(e)}")

def get_session():
    """Get a new database session"""
    return SessionLocal()

def validate_product_data(data: dict) -> None:
    """Validate product data before insertion"""
    try:
        Product.validate_data(data)
    except ValidationError as e:
        raise ValidationError(f"Product validation failed: {str(e)}")

def validate_price_data(data: dict) -> None:
    """Validate price history data before insertion"""
    try:
        PriceHistory.validate_data(data)
    except ValidationError as e:
        raise ValidationError(f"Price history validation failed: {str(e)}")
