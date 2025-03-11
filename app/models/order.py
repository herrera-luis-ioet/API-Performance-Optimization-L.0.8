"""Order models.

This module defines the SQLAlchemy models for orders and order items.
"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    Column,
    Enum as SQLAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, relationship

from app.db.base import Base


class OrderStatus(str, Enum):
    """Order status enum.
    
    Defines the possible statuses for an order.
    """
    
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    """Order model.
    
    Represents an order in the system with all its attributes.
    """
    
    # Order information
    status: Mapped[OrderStatus] = Column(
        SQLAEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True
    )
    total_amount: Mapped[Decimal] = Column(
        Numeric(precision=10, scale=2), nullable=False, default=0.0
    )
    
    # Customer information
    customer_email: Mapped[str] = Column(String(255), nullable=False)
    customer_name: Mapped[str] = Column(String(255), nullable=False)
    
    # Shipping information
    shipping_address: Mapped[Optional[str]] = Column(Text, nullable=True)
    shipping_city: Mapped[Optional[str]] = Column(String(100), nullable=True)
    shipping_country: Mapped[Optional[str]] = Column(String(100), nullable=True)
    shipping_postal_code: Mapped[Optional[str]] = Column(String(20), nullable=True)
    
    # Payment information
    payment_method: Mapped[Optional[str]] = Column(String(50), nullable=True)
    payment_id: Mapped[Optional[str]] = Column(String(100), nullable=True)
    
    # Additional information
    notes: Mapped[Optional[str]] = Column(Text, nullable=True)
    
    # Relationships
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    
    # No composite index needed after removing customer_id
    __table_args__ = ()
    
    def __repr__(self) -> str:
        """String representation of the order.
        
        Returns:
            str: String representation
        """
        return f"<Order(id={self.id}, status='{self.status}', total_amount={self.total_amount})>"


class OrderItem(Base):
    """Order item model.
    
    Represents an item in an order, linking orders and products.
    """
    
    # Order relationship
    order_id: Mapped[int] = Column(
        Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False, index=True
    )
    order: Mapped[Order] = relationship("Order", back_populates="items")
    
    # Product relationship
    product_id: Mapped[int] = Column(
        Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    
    # Item details
    quantity: Mapped[int] = Column(Integer, nullable=False, default=1)
    price_at_purchase: Mapped[Decimal] = Column(
        Numeric(precision=10, scale=2), nullable=False
    )
    
    # Additional information
    product_name: Mapped[str] = Column(String(255), nullable=False)
    product_sku: Mapped[str] = Column(String(50), nullable=False)
    
    # Create composite index for common query patterns
    __table_args__ = (
        Index("idx_order_item_order_product", "order_id", "product_id"),
    )
    
    def __repr__(self) -> str:
        """String representation of the order item.
        
        Returns:
            str: String representation
        """
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
