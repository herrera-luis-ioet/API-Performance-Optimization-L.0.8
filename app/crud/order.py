from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime, timedelta

from app.crud.base import BaseCRUD
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead, OrderItemCreate

logger = logging.getLogger(__name__)


class OrderCRUD(BaseCRUD[Order, OrderCreate, OrderUpdate, OrderRead]):
    """
    CRUD operations for Order model.
    
    Extends the BaseCRUD class with order-specific operations.
    """
    
    # PUBLIC_INTERFACE
    async def create_with_items(
        self, db: AsyncSession, *, obj_in: OrderCreate
    ) -> Order:
        """
        Create a new order with its items.
        
        Args:
            db: Database session
            obj_in: Input data for creating the order with items
            
        Returns:
            The created order
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            # Start a transaction
            async with db.begin():
                # Create order without items first
                order_data = obj_in.model_dump(exclude={"items"})
                db_order = Order(**order_data)
                db.add(db_order)
                await db.flush()  # Flush to get the order ID
                
                # Create order items
                for item_data in obj_in.items:
                    db_item = OrderItem(
                        order_id=db_order.id,
                        **item_data.model_dump()
                    )
                    db.add(db_item)
                
                await db.commit()
                await db.refresh(db_order)
                return db_order
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error creating order with items: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_with_items(
        self, db: AsyncSession, *, order_id: int
    ) -> Optional[Order]:
        """
        Get an order with its items.
        
        Args:
            db: Database session
            order_id: ID of the order to get
            
        Returns:
            The order with items if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(Order).where(Order.id == order_id)
            result = await db.execute(query)
            order = result.scalars().first()
            
            if order:
                # Load items relationship
                await db.refresh(order, ["items"])
            
            return order
        except SQLAlchemyError as e:
            logger.error(f"Error getting order with items for order ID {order_id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def update_status(
        self, db: AsyncSession, *, order_id: int, status: OrderStatus
    ) -> Optional[Order]:
        """
        Update the status of an order.
        
        Args:
            db: Database session
            order_id: ID of the order to update
            status: New status for the order
            
        Returns:
            The updated order if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            order = await self.get(db=db, id=order_id)
            if not order:
                return None
            
            order.status = status
            db.add(order)
            await db.commit()
            await db.refresh(order)
            return order
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error updating status for order {order_id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_by_customer(
        self, db: AsyncSession, *, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Get orders for a specific customer with pagination.
        
        Args:
            db: Database session
            customer_id: ID of the customer
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders for the specified customer
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.customer_id == customer_id).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders for customer {customer_id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_by_status(
        self, db: AsyncSession, *, status: OrderStatus, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Get orders with a specific status with pagination.
        
        Args:
            db: Database session
            status: Order status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders with the specified status
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.status == status).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders with status {status}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_by_date_range(
        self, db: AsyncSession, *, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Get orders within a date range with pagination.
        
        Args:
            db: Database session
            start_date: Start date for the range
            end_date: End date for the range
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders within the specified date range
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(
                and_(
                    self.model.created_at >= start_date,
                    self.model.created_at <= end_date
                )
            ).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders in date range {start_date} to {end_date}: {str(e)}")
            raise


class OrderItemCRUD(BaseCRUD[OrderItem, OrderItemCreate, Dict[str, Any], Dict[str, Any]]):
    """
    CRUD operations for OrderItem model.
    
    Extends the BaseCRUD class with order item-specific operations.
    """
    
    # PUBLIC_INTERFACE
    async def get_by_order(
        self, db: AsyncSession, *, order_id: int
    ) -> List[OrderItem]:
        """
        Get all items for a specific order.
        
        Args:
            db: Database session
            order_id: ID of the order
            
        Returns:
            List of order items for the specified order
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.order_id == order_id)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting items for order {order_id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_by_product(
        self, db: AsyncSession, *, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderItem]:
        """
        Get all order items for a specific product with pagination.
        
        Args:
            db: Database session
            product_id: ID of the product
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of order items for the specified product
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.product_id == product_id).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting order items for product {product_id}: {str(e)}")
            raise


# Create singleton instances
order = OrderCRUD(Order)
order_item = OrderItemCRUD(OrderItem)