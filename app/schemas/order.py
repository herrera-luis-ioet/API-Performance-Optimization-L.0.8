"""Order schemas.

This module defines Pydantic schemas for order and order item validation.
"""

from decimal import Decimal
from typing import List, Optional

from pydantic import Field, field_validator, EmailStr

from app.models.order import OrderStatus
from app.schemas import BaseCreateSchema, BaseReadSchema, BaseSchema, BaseUpdateSchema


class OrderItemBase(BaseSchema):
    """Base schema for order item data.
    
    Contains fields common to all order item schemas.
    """
    
    product_id: int = Field(
        ..., 
        description="Product ID", 
        gt=0,
        examples=[1]
    )
    quantity: int = Field(
        1, 
        description="Quantity of the product", 
        gt=0,
        examples=[2]
    )
    product_name: Optional[str] = Field(
        None, 
        description="Product name at the time of purchase",
        examples=["Ergonomic Keyboard"]
    )
    product_sku: Optional[str] = Field(
        None, 
        description="Product SKU at the time of purchase",
        examples=["ERG-KB-001"]
    )
    price_at_purchase: Optional[Decimal] = Field(
        None, 
        description="Product price at the time of purchase", 
        ge=0,
        examples=[99.99]
    )
    
    @field_validator("price_at_purchase")
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


class OrderItemCreate(OrderItemBase, BaseCreateSchema):
    """Schema for creating a new order item.
    
    Inherits all fields from OrderItemBase.
    Only product_id and quantity are required for creation.
    """
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "quantity": 2
            }
        }
    }


class OrderItemUpdate(BaseUpdateSchema):
    """Schema for updating an existing order item.
    
    All fields are optional to allow partial updates.
    """
    
    quantity: Optional[int] = Field(
        None, 
        description="Quantity of the product", 
        gt=0
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "quantity": 3
            }
        }
    }


class OrderItemRead(OrderItemBase, BaseReadSchema):
    """Schema for reading order item data.
    
    Inherits all fields from OrderItemBase and BaseReadSchema.
    """
    
    order_id: int = Field(..., description="Order ID")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "order_id": 1,
                "product_id": 1,
                "quantity": 2,
                "product_name": "Ergonomic Keyboard",
                "product_sku": "ERG-KB-001",
                "price_at_purchase": 99.99,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    }


class OrderBase(BaseSchema):
    """Base schema for order data.
    
    Contains fields common to all order schemas.
    """
    
    status: OrderStatus = Field(
        OrderStatus.PENDING, 
        description="Order status",
        examples=[OrderStatus.PENDING]
    )
    total_amount: Decimal = Field(
        0.0, 
        description="Total order amount", 
        ge=0,
        examples=[199.98]
    )
    customer_id: Optional[int] = Field(
        None, 
        description="Customer ID", 
        gt=0,
        examples=[1]
    )
    customer_email: EmailStr = Field(
        ..., 
        description="Customer email address",
        examples=["customer@example.com"]
    )
    customer_name: str = Field(
        ..., 
        description="Customer name", 
        min_length=1, 
        max_length=255,
        examples=["John Doe"]
    )
    shipping_address: Optional[str] = Field(
        None, 
        description="Shipping address",
        examples=["123 Main St, Apt 4B"]
    )
    shipping_city: Optional[str] = Field(
        None, 
        description="Shipping city", 
        max_length=100,
        examples=["New York"]
    )
    shipping_country: Optional[str] = Field(
        None, 
        description="Shipping country", 
        max_length=100,
        examples=["USA"]
    )
    shipping_postal_code: Optional[str] = Field(
        None, 
        description="Shipping postal code", 
        max_length=20,
        examples=["10001"]
    )
    payment_method: Optional[str] = Field(
        None, 
        description="Payment method", 
        max_length=50,
        examples=["credit_card"]
    )
    payment_id: Optional[str] = Field(
        None, 
        description="Payment ID", 
        max_length=100,
        examples=["pay_123456789"]
    )
    notes: Optional[str] = Field(
        None, 
        description="Additional notes",
        examples=["Please leave package at the door"]
    )
    
    @field_validator("total_amount")
    @classmethod
    def validate_total_amount(cls, v: Decimal) -> Decimal:
        """Validate that total amount has at most 2 decimal places.
        
        Args:
            v: The total amount value to validate
            
        Returns:
            The validated total amount
            
        Raises:
            ValueError: If total amount has more than 2 decimal places
        """
        if v.quantize(Decimal("0.01")) != v:
            raise ValueError("Total amount must have at most 2 decimal places")
        return v


class OrderCreate(OrderBase, BaseCreateSchema):
    """Schema for creating a new order.
    
    Inherits all fields from OrderBase and adds items field.
    """
    
    items: List[OrderItemCreate] = Field(
        ..., 
        description="Order items",
        min_length=1
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_email": "customer@example.com",
                "customer_name": "John Doe",
                "shipping_address": "123 Main St, Apt 4B",
                "shipping_city": "New York",
                "shipping_country": "USA",
                "shipping_postal_code": "10001",
                "payment_method": "credit_card",
                "payment_id": "pay_123456789",
                "notes": "Please leave package at the door",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2
                    }
                ]
            }
        }
    }


class OrderUpdate(BaseUpdateSchema):
    """Schema for updating an existing order.
    
    All fields are optional to allow partial updates.
    """
    
    status: Optional[OrderStatus] = Field(
        None, 
        description="Order status"
    )
    customer_email: Optional[EmailStr] = Field(
        None, 
        description="Customer email address"
    )
    customer_name: Optional[str] = Field(
        None, 
        description="Customer name", 
        min_length=1, 
        max_length=255
    )
    shipping_address: Optional[str] = Field(
        None, 
        description="Shipping address"
    )
    shipping_city: Optional[str] = Field(
        None, 
        description="Shipping city", 
        max_length=100
    )
    shipping_country: Optional[str] = Field(
        None, 
        description="Shipping country", 
        max_length=100
    )
    shipping_postal_code: Optional[str] = Field(
        None, 
        description="Shipping postal code", 
        max_length=20
    )
    payment_method: Optional[str] = Field(
        None, 
        description="Payment method", 
        max_length=50
    )
    payment_id: Optional[str] = Field(
        None, 
        description="Payment ID", 
        max_length=100
    )
    notes: Optional[str] = Field(
        None, 
        description="Additional notes"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "processing",
                "shipping_address": "456 New St, Suite 7C",
                "notes": "Updated delivery instructions"
            }
        }
    }


class OrderRead(OrderBase, BaseReadSchema):
    """Schema for reading order data.
    
    Inherits all fields from OrderBase and BaseReadSchema.
    Adds items field for related order items.
    """
    
    items: List[OrderItemRead] = Field(
        [], 
        description="Order items"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "status": "pending",
                "total_amount": 199.98,
                "customer_id": 1,
                "customer_email": "customer@example.com",
                "customer_name": "John Doe",
                "shipping_address": "123 Main St, Apt 4B",
                "shipping_city": "New York",
                "shipping_country": "USA",
                "shipping_postal_code": "10001",
                "payment_method": "credit_card",
                "payment_id": "pay_123456789",
                "notes": "Please leave package at the door",
                "items": [
                    {
                        "id": 1,
                        "order_id": 1,
                        "product_id": 1,
                        "quantity": 2,
                        "product_name": "Ergonomic Keyboard",
                        "product_sku": "ERG-KB-001",
                        "price_at_purchase": 99.99,
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00"
                    }
                ],
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    }