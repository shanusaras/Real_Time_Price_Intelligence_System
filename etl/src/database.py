"""
Database configuration and models for the Price Intelligence System.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
from urllib.parse import quote_plus

# URL encode the password to handle special characters
password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE')}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="category_rel")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    brand = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    link = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category_rel = relationship("Category", back_populates="products")
    prices = relationship("Price", back_populates="product")

class Price(Base):
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float, nullable=False)
    discount_pct = Column(Integer, default=0)
    in_stock = Column(Boolean, default=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="prices")

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
