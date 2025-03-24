"""Base schema classes for Pydantic models.

This module defines base Pydantic schema classes for common operations
like create, update, and read.
"""

from datetime import datetime
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base schema class for all Pydantic models.
    
    Provides common configuration and functionality for all schemas.
    """
    
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        json_schema_extra={"example": {}},
    )


class BaseCreateSchema(BaseSchema):
    """Base schema for create operations.
    
    Used as a base class for all create operation schemas.
    """
    
    pass


class BaseUpdateSchema(BaseSchema):
    """Base schema for update operations.
    
    Used as a base class for all update operation schemas.
    All fields are optional to allow partial updates.
    """
    
    pass


class BaseReadSchema(BaseSchema):
    """Base schema for read operations.
    
    Used as a base class for all read operation schemas.
    Includes common fields like id and timestamps.
    """
    
    id: int = Field(..., description="Unique identifier")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")


# Type variable for use with Generic schemas
T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response schema.
    
    Generic schema for paginated responses.
    """
    
    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
