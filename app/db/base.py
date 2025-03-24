"""Base model for SQLAlchemy models.

This module provides a base model class with common fields and functionality
that all models in the application will inherit from.
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    This class provides common fields and functionality that all models will inherit.
    """

    # Make tablename automatically generated from class name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name.

        Returns:
            str: Table name in snake_case
        """
        # Convert CamelCase to snake_case
        name = cls.__name__
        return "".join(
            ["_" + c.lower() if c.isupper() else c for c in name]
        ).lstrip("_")

    # Common columns for all models
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    createdAt: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
