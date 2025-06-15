from pydantic import Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from .base import BaseSchema, TimestampMixin

if TYPE_CHECKING:
    from .product import ProductNested

class CategoryBase(BaseSchema):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=120)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryInDB(CategoryBase, TimestampMixin):
    id: int
    # Use string literals for forward references
    products: List['ProductNested'] = []
    
    model_config = ConfigDict(from_attributes=True)

# This will be used to avoid circular imports
class CategoryNested(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
