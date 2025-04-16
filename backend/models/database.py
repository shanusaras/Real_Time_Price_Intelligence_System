from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    description = Column(String(1000))
    rating = Column(Float)  # Product rating (0-5)
    review_count = Column(Integer)  # Number of reviews
    features = Column(Text)  # Product features/specifications
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = relationship("PriceHistory", back_populates="product")
    analytics = relationship("ProductAnalytics", back_populates="product", uselist=False)

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float, nullable=False)
    original_price = Column(Float)  # Price before discount
    discount_percentage = Column(Float)  # Calculated discount %
    currency = Column(String(3), default="INR")
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50))  # e.g., "flipkart", "amazon", etc.
    url = Column(String(500))  # Product URL
    
    # Relationships
    product = relationship("Product", back_populates="prices")

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    competitor_name = Column(String(100))
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    timestamp = Column(DateTime, default=datetime.utcnow)
    url = Column(String(500))

# Database connection
def get_engine(database_url: str):
    return create_engine(database_url)

class ProductAnalytics(Base):
    __tablename__ = "product_analytics"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True)
    avg_price = Column(Float)  # Rolling average price
    price_volatility = Column(Float)  # Price change frequency
    price_range = Column(String(50))  # Price bracket/range
    competitor_count = Column(Integer)  # Number of competitors
    market_position = Column(String(50))  # e.g., "premium", "budget"
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="analytics")

def init_db(engine):
    Base.metadata.create_all(engine)
