from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar('T')

class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        },
        populate_by_name=True
    )

class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Message(BaseModel):
    """Standard message response schema."""
    message: str = Field(..., description="A message describing the result of the operation")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"message": "Operation completed successfully"}
        }
    )

class ResponseModel(BaseModel, Generic[T]):
    """Standard response model with data and metadata."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": None
            }
        }
    )
