from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String, Text, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel

if TYPE_CHECKING:
    from .product import Product

class Category(BaseModel, Base):
    """
    Category model for product categorization.
    
    Supports hierarchical categories with parent-child relationships.
    """
    __tablename__ = 'categories'
    
    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id'), 
        nullable=True, 
        index=True
    )
    
    # Relationships
    parent: Mapped[Optional['Category']] = relationship(
        'Category', 
        remote_side='Category.id',
        back_populates='subcategories',
        uselist=False
    )
    
    subcategories: Mapped[List['Category']] = relationship(
        'Category',
        back_populates='parent',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    
    products: Mapped[List['Product']] = relationship(
        'Product', 
        back_populates='category',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"
