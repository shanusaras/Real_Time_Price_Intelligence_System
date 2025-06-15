from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from .base import BaseSchema, TimestampMixin

# Import for type checking only
if TYPE_CHECKING:
    from .product import ProductNested

class PriceBase(BaseSchema):
    product_id: int
    price: float = Field(..., gt=0)
    original_price: Optional[float] = None
    discount: Optional[float] = None
    in_stock: Optional[int] = 0
    currency: str = "KES"

class PriceCreate(PriceBase):
    pass

class PriceUpdate(BaseSchema):
    price: Optional[float] = Field(None, gt=0)
    original_price: Optional[float] = None
    discount: Optional[float] = None
    in_stock: Optional[int] = None
    currency: Optional[str] = None

class PriceInDB(PriceBase, TimestampMixin):
    id: int
    product: Optional['ProductNested'] = None
    
    model_config = ConfigDict(from_attributes=True)
