from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DB_CONFIG
from urllib.parse import quote_plus

import os
# print("DEBUG: MYSQL_PASSWORD from env =", os.environ.get("MYSQL_PASSWORD"))

# Build the MySQL connection URL with URL-encoded password
password = quote_plus(DB_CONFIG['password'])
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{password}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    link = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    price_history = relationship('PriceHistory', back_populates='product')

class PriceHistory(Base):
    __tablename__ = 'price_history'
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    discount_pct = Column(DECIMAL(5, 2), default=0)
    in_stock = Column(Boolean, default=True)
    rating = Column(Float)
    reviews = Column(Integer, default=0)
    scraped_at = Column(DateTime, server_default=func.now())
    product = relationship('Product', back_populates='price_history')

# Create tables if they don't exist
def create_tables():
    Base.metadata.create_all(engine)
