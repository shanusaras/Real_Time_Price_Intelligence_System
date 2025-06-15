from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String, Text, Index, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel

if TYPE_CHECKING:
    from .category import Category
    from .price import Price

class Product(BaseModel, Base):
    """
    Product model for storing product information.
    
    Represents a product that can be tracked for price changes.
    """
    __tablename__ = 'products'
    
    # Columns
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'), 
        nullable=False, 
        index=True
    )
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    category: Mapped['Category'] = relationship(
        'Category', 
        back_populates='products',
        lazy='selectin'
    )
    
    prices: Mapped[List['Price']] = relationship(
        'Price', 
        back_populates='product',
        cascade='all, delete-orphan',
        lazy='selectin',
        order_by='desc(Price.created_at)'
    )
    
    # Indexes
    __table_args__ = (
        Index('ix_products_name_category', 'name', 'category_id'),
        Index('ix_products_brand_category', 'brand', 'category_id'),
    )
    
    @property
    def current_price(self) -> Optional['Price']:
        """Get the most recent price for this product."""
        return self.prices[0] if self.prices else None
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"
