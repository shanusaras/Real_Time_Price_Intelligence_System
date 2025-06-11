from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, desc
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    discount = Column(Float)
    category = Column(String(200), index=True)
    subcategory = Column(String(200), index=True)
    brand = Column(String(200), index=True)
    rating = Column(Float)
    review_count = Column(Integer)
    url = Column(String(1000))
    image_url = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    parent_category = Column(String(200), index=True)
    product_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
