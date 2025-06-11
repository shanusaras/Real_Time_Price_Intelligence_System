from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, validator

class ProductBase(BaseModel):
    """Base model for product data"""
    name: str
    brand: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    url: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    price: float
    original_price: Optional[float] = None
    discount: Optional[float] = None
    rating: Optional[float] = None
    review_count: int = 0

class Product(ProductBase):
    """Schema for product response"""
    id: int
    price: float
    original_price: Optional[float] = None
    discount: Optional[float] = None
    rating: Optional[float] = None
    review_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class PriceHistoryBase(BaseModel):
    """Base model for price history"""
    product_id: int
    price: float = Field(..., gt=0, description="Price must be greater than 0")

class PriceHistoryCreate(PriceHistoryBase):
    """Schema for creating new price history"""
    pass

class PriceHistory(PriceHistoryBase):
    """Schema for price history response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductWithPrice(Product):
    """Schema for product with latest price information"""
    current_price: Optional[float] = None
    original_price: Optional[float] = None
    discount: Optional[float] = None
    in_stock: bool = True
    rating: Optional[float] = None
    review_count: int = 0
    last_updated: Optional[datetime] = None

class ProductListResponse(BaseModel):
    """Response schema for product list with pagination"""
    count: int
    total: int
    offset: int
    limit: int
    results: List[ProductWithPrice]

class PriceHistoryResponse(BaseModel):
    """Response schema for price history"""
    product_id: int
    product_name: str
    history: List[PriceHistory]

class CategoryStats(BaseModel):
    """Schema for category statistics"""
    category: str
    product_count: int
    min_price: float
    max_price: float
    avg_price: float
    avg_rating: Optional[float]

class AnalyticsSummary(BaseModel):
    """Schema for analytics summary"""
    total_products: int
    total_categories: int
    avg_price: float
    avg_rating: Optional[float]
    total_reviews: int
    last_updated: datetime
