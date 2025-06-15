from pydantic import Field, HttpUrl, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from .base import BaseSchema, TimestampMixin

# Import for type checking only
if TYPE_CHECKING:
    from .category import CategoryNested

class ProductBase(BaseSchema):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    brand: Optional[str] = Field(None, max_length=100)
    category_id: int
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

class ProductCreate(ProductBase):
    price: Optional[float] = None
    original_price: Optional[float] = None
    discount: Optional[float] = None
    in_stock: Optional[int] = None

class ProductUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    brand: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    discount: Optional[float] = None
    in_stock: Optional[int] = None

class ProductInDB(ProductBase, TimestampMixin):
    id: int
    category: Optional['CategoryNested'] = None
    
    model_config = ConfigDict(from_attributes=True)

# This will be used to avoid circular imports
class ProductNested(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
