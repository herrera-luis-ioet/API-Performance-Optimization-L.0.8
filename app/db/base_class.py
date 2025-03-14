"""Base class for SQLAlchemy models.

This module imports all models to ensure they are registered with SQLAlchemy's metadata.
"""

from app.db.base import Base
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus

# Make sure all models are imported here to ensure they are registered with SQLAlchemy's metadata
__all__ = [
    "Base",
    "Product",
    "Order",
    "OrderItem",
    "OrderStatus",
]