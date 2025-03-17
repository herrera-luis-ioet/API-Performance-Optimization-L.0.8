"""Product schemas.

This module defines Pydantic schemas for product validation.
"""

from decimal import Decimal
from typing import List, Optional

from pydantic import Field, field_validator

from app.schemas import BaseCreateSchema, BaseReadSchema, BaseSchema, BaseUpdateSchema


class ProductBase(BaseSchema):
    """Base schema for product data.
    
    Contains fields common to all product schemas.
    """
    
    name: str = Field(
        ..., 
        description="Product name", 
        min_length=1, 
        max_length=255,
        examples=["Ergonomic Keyboard"]
    )
    description: Optional[str] = Field(
        None, 
        description="Product description",
        examples=["Comfortable keyboard with ergonomic design"]
    )
    sku: str = Field(
        ..., 
        description="Stock keeping unit (unique identifier)", 
        min_length=3, 
        max_length=50,
        pattern=r"^[A-Za-z0-9\-_]+$",
        examples=["ERG-KB-001"]
    )
    image: Optional[str] = Field(
        None,
        description="URL or path to product image",
        max_length=255,
        examples=["https://example.com/images/ergonomic-keyboard.jpg"]
    )
    mainImage: Optional[str] = Field(
        None,
        description="URL or path to main product image",
        max_length=255,
        examples=["https://example.com/images/ergonomic-keyboard-main.jpg"]
    )
    price: Decimal = Field(
        ..., 
        description="Product price", 
        ge=0, 
        examples=[99.99]
    )
    stock: int = Field(
        0, 
        description="Available stock quantity", 
        ge=0,
        examples=[100]
    )
    category: Optional[str] = Field(
        None, 
        description="Product category", 
        max_length=100,
        examples=["Electronics"]
    )
    tags: Optional[str] = Field(
        None, 
        description="Comma-separated tags", 
        max_length=255,
        examples=["ergonomic,keyboard,office"]
    )
    is_active: bool = Field(
        True, 
        description="Whether the product is active"
    )
    rating: Optional[int] = Field(
        None,
        description="Product rating (1-5)",
        ge=1,
        le=5,
        examples=[4]
    )
    ratingCount: int = Field(
        0,
        description="Number of ratings received",
        ge=0,
        examples=[42]
    )
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        """Validate that price has at most 2 decimal places.
        
        Args:
            v: The price value to validate
            
        Returns:
            The validated price
            
        Raises:
            ValueError: If price has more than 2 decimal places
        """
        if v.quantize(Decimal("0.01")) != v:
            raise ValueError("Price must have at most 2 decimal places")
        return v


class ProductCreate(ProductBase, BaseCreateSchema):
    """Schema for creating a new product.
    
    Inherits all fields from ProductBase.
    """
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ergonomic Keyboard",
                "description": "Comfortable keyboard with ergonomic design",
                "sku": "ERG-KB-001",
                "image": "https://example.com/images/ergonomic-keyboard.jpg",
                "mainImage": "https://example.com/images/ergonomic-keyboard-main.jpg",
                "price": 99.99,
                "stock": 100,
                "category": "Electronics",
                "tags": "ergonomic,keyboard,office",
                "is_active": True,
                "rating": 4,
                "ratingCount": 0
            }
        }
    }


class ProductUpdate(BaseUpdateSchema):
    """Schema for updating an existing product.
    
    All fields are optional to allow partial updates.
    """
    
    name: Optional[str] = Field(
        None, 
        description="Product name", 
        min_length=1, 
        max_length=255
    )
    description: Optional[str] = Field(
        None, 
        description="Product description"
    )
    sku: Optional[str] = Field(
        None, 
        description="Stock keeping unit (unique identifier)", 
        min_length=3, 
        max_length=50,
        pattern=r"^[A-Za-z0-9\-_]+$"
    )
    image: Optional[str] = Field(
        None,
        description="URL or path to product image",
        max_length=255
    )
    mainImage: Optional[str] = Field(
        None,
        description="URL or path to main product image",
        max_length=255
    )
    price: Optional[Decimal] = Field(
        None, 
        description="Product price", 
        ge=0
    )
    stock: Optional[int] = Field(
        None, 
        description="Available stock quantity", 
        ge=0
    )
    category: Optional[str] = Field(
        None, 
        description="Product category", 
        max_length=100
    )
    tags: Optional[str] = Field(
        None, 
        description="Comma-separated tags", 
        max_length=255
    )
    is_active: Optional[bool] = Field(
        None, 
        description="Whether the product is active"
    )
    rating: Optional[int] = Field(
        None,
        description="Product rating (1-5)",
        ge=1,
        le=5
    )
    ratingCount: Optional[int] = Field(
        None,
        description="Number of ratings received",
        ge=0
    )
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Validate that price has at most 2 decimal places.
        
        Args:
            v: The price value to validate
            
        Returns:
            The validated price
            
        Raises:
            ValueError: If price has more than 2 decimal places
        """
        if v is not None and v.quantize(Decimal("0.01")) != v:
            raise ValueError("Price must have at most 2 decimal places")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "price": 89.99,
                "stock": 150,
                "image": "https://example.com/images/updated-keyboard.jpg",
                "mainImage": "https://example.com/images/updated-keyboard-main.jpg",
                "is_active": True
            }
        }
    }


class ProductRead(ProductBase, BaseReadSchema):
    """Schema for reading product data.
    
    Inherits all fields from ProductBase and BaseReadSchema.
    """
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Ergonomic Keyboard",
                "description": "Comfortable keyboard with ergonomic design",
                "sku": "ERG-KB-001",
                "image": "https://example.com/images/ergonomic-keyboard.jpg",
                "mainImage": "https://example.com/images/ergonomic-keyboard-main.jpg",
                "price": 99.99,
                "stock": 100,
                "category": "Electronics",
                "tags": "ergonomic,keyboard,office",
                "is_active": True,
                "rating": 4,
                "ratingCount": 42,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    }
