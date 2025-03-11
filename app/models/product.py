"""Product model.

This module defines the SQLAlchemy model for products.
"""

from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, relationship

from app.db.base import Base


class Product(Base):
    """Product model.

    Represents a product in the system with all its attributes.
    """

    # Basic product information
    name: Mapped[str] = Column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    sku: Mapped[str] = Column(String(50), nullable=False, unique=True, index=True)
    image: Mapped[Optional[str]] = Column(String(255), nullable=True)
    price: Mapped[Decimal] = Column(
        Numeric(precision=10, scale=2), nullable=False, default=0.0
    )
    
    # Inventory information
    stock_quantity: Mapped[int] = Column(Integer, nullable=False, default=0)
    
    # Categorization
    category: Mapped[Optional[str]] = Column(String(100), nullable=True, index=True)
    tags: Mapped[Optional[str]] = Column(String(255), nullable=True)
    
    # Status
    is_active: Mapped[bool] = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
    
    # Create composite index for common query patterns
    __table_args__ = (
        Index("idx_product_category_active", "category", "is_active"),
    )
    
    def __repr__(self) -> str:
        """String representation of the product.
        
        Returns:
            str: String representation
        """
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
