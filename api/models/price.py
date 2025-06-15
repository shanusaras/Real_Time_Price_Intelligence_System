from datetime import datetime
from typing import TYPE_CHECKING, Optional
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, Integer, Index, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base, BaseModel

if TYPE_CHECKING:
    from .product import Product

class Price(BaseModel, Base):
    """
    Price model for tracking price history of products.
    
    Each record represents a price point in time for a product.
    """
    __tablename__ = 'prices'
    
    # Columns
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Using Numeric for precise decimal calculations
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment='Current price of the product'
    )
    
    original_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        comment='Original price before any discounts'
    )
    
    discount: Mapped[Optional[float]] = mapped_column(
        comment='Discount percentage (0-100)'
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        default='KES',
        index=True,
        comment='Currency code (ISO 4217)'
    )
    
    in_stock: Mapped[bool] = mapped_column(
        default=True,
        index=True,
        comment='Product availability status'
    )
    
    stock_quantity: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment='Available quantity in stock (if known)'
    )
    
    # Relationships
    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='prices',
        lazy='selectin'
    )
    
    # Indexes
    __table_args__ = (
        Index('ix_prices_product_created', 'product_id', 'created_at'),
        Index('ix_prices_created', 'created_at'),
    )
    
    @property
    def discount_amount(self) -> Optional[Decimal]:
        """Calculate the discount amount if original price is available."""
        if self.original_price is not None and self.discount:
            return Decimal(str(self.original_price)) - self.price
        return None
    
    def __repr__(self) -> str:
        return f"<Price(id={self.id}, product_id={self.product_id}, price={self.price} {self.currency})>"
