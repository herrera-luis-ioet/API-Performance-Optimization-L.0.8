from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.crud.base import BaseCRUD
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead

logger = logging.getLogger(__name__)


class ProductCRUD(BaseCRUD[Product, ProductCreate, ProductUpdate, ProductRead]):
    """
    CRUD operations for Product model.
    
    Extends the BaseCRUD class with product-specific operations.
    """
    
    # PUBLIC_INTERFACE
    async def get_by_sku(self, db: AsyncSession, *, sku: str) -> Optional[Product]:
        """
        Get a product by its SKU.
        
        Args:
            db: Database session
            sku: Product SKU
            
        Returns:
            The product if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.sku == sku)
            result = await db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting product with SKU {sku}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_by_category(
        self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get products by category with pagination.
        
        Args:
            db: Database session
            category: Product category
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of products in the specified category
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.category == category).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting products in category {category}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def update_stock(
        self, db: AsyncSession, *, product_id: int, quantity_change: int
    ) -> Optional[Product]:
        """
        Update product stock quantity.
        
        Args:
            db: Database session
            product_id: ID of the product to update
            quantity_change: Amount to add to the stock (can be negative)
            
        Returns:
            The updated product if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
            ValueError: If the resulting stock quantity would be negative
        """
        try:
            product = await self.get(db=db, id=product_id)
            if not product:
                return None
            
            new_quantity = product.stock + quantity_change
            if new_quantity < 0:
                raise ValueError(f"Cannot reduce stock below zero for product {product_id}")
            
            product.stock = new_quantity
            db.add(product)
            await db.commit()
            await db.refresh(product)
            return product
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error updating stock for product {product_id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_active(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get active products with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active products
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.is_active == True).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting active products: {str(e)}")
            raise


# Create a singleton instance
product = ProductCRUD(Product)
