"""
Database models for the Price Intelligence System.

This module contains all SQLAlchemy models used in the application.
"""
from typing import TYPE_CHECKING

# Import base classes first to avoid circular imports
from .base import Base, BaseModel

# Import models
from .category import Category
from .product import Product
from .price import Price

# Set up relationships after all models are defined
if not TYPE_CHECKING:
    # This is a workaround for circular imports
    # The actual relationship setup is done in each model file
    pass

__all__ = [
    'Base',
    'BaseModel',
    'Category',
    'Product',
    'Price',
]
