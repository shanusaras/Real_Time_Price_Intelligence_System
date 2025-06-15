from datetime import datetime
from typing import Any
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Uses SQLAlchemy 2.0 style with type annotations.
    """
    pass

class BaseModel:
    """
    Abstract base model with common columns and functionality.
    All database models should inherit from this class.
    """
    __abstract__ = True
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Table naming convention - pluralized model name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
    
    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
