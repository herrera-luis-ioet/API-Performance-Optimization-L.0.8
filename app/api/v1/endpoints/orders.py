"""Order API endpoints.

This module defines the API endpoints for order operations.
"""

from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination_params, handle_db_exceptions, ErrorResponse
from app.core.rate_limit import rate_limit
from app.crud.order import order, order_item
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

# Create router for order endpoints
router = APIRouter()


@router.get(
    "/",
    response_model=List[OrderRead],
    summary="Get all orders",
    description="Retrieve a list of all orders with pagination",
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def get_orders(
    request: Request,
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get all orders with pagination.
    
    Args:
        request: FastAPI request object
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of orders
    """
    return await order.get_multi(db, skip=pagination["skip"], limit=pagination["limit"])


@router.get(
    "/customer/{customer_id}",
    response_model=List[OrderRead],
    summary="Get orders by customer",
    description="Retrieve a list of orders for a specific customer with pagination",
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def get_orders_by_customer(
    request: Request,
    customer_id: int = Path(..., description="Customer ID"),
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get orders by customer with pagination.
    
    Args:
        request: FastAPI request object
        customer_id: Customer ID
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of orders for the specified customer
    """
    return await order.get_by_customer(
        db, customer_id=customer_id, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get(
    "/status/{status}",
    response_model=List[OrderRead],
    summary="Get orders by status",
    description="Retrieve a list of orders with a specific status with pagination",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid status"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def get_orders_by_status(
    request: Request,
    status: OrderStatus = Path(..., description="Order status"),
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get orders by status with pagination.
    
    Args:
        request: FastAPI request object
        status: Order status
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of orders with the specified status
    """
    return await order.get_by_status(
        db, status=status, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get(
    "/date-range",
    response_model=List[OrderRead],
    summary="Get orders by date range",
    description="Retrieve a list of orders within a specific date range with pagination",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid date range"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def get_orders_by_date_range(
    request: Request,
    start_date: datetime = Query(..., description="Start date (ISO format)"),
    end_date: datetime = Query(..., description="End date (ISO format)"),
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get orders by date range with pagination.
    
    Args:
        request: FastAPI request object
        start_date: Start date
        end_date: End date
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of orders within the specified date range
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    return await order.get_by_date_range(
        db, start_date=start_date, end_date=end_date, 
        skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    summary="Get order by ID",
    description="Retrieve an order by its ID with its items",
    responses={
        404: {"model": ErrorResponse, "description": "Order not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def get_order(
    request: Request,
    order_id: int = Path(..., description="Order ID"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get an order by its ID with its items.
    
    Args:
        request: FastAPI request object
        order_id: Order ID
        db: Database session
        
    Returns:
        Order with the specified ID and its items
    """
    db_order = await order.get_with_items(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return db_order


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create order",
    description="Create a new order with items",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def create_order(
    request: Request,
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new order with items.
    
    Args:
        request: FastAPI request object
        order_in: Order data with items
        db: Database session
        
    Returns:
        Created order with items
    """
    # Validate that order has at least one item
    if not order_in.items or len(order_in.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must have at least one item"
        )
    
    db_order = await order.create_with_items(db, obj_in=order_in)
    return await order.get_with_items(db, order_id=db_order.id)


@router.put(
    "/{order_id}",
    response_model=OrderRead,
    summary="Update order",
    description="Update an order by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Order not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def update_order(
    request: Request,
    order_in: OrderUpdate,
    order_id: int = Path(..., description="Order ID"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update an order.
    
    Args:
        request: FastAPI request object
        order_in: Order data to update
        order_id: Order ID
        db: Database session
        
    Returns:
        Updated order
    """
    db_order = await order.get(db, id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    updated_order = await order.update(db, db_obj=db_order, obj_in=order_in)
    return await order.get_with_items(db, order_id=updated_order.id)


@router.patch(
    "/{order_id}/status",
    response_model=OrderRead,
    summary="Update order status",
    description="Update an order's status",
    responses={
        404: {"model": ErrorResponse, "description": "Order not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def update_order_status(
    request: Request,
    order_id: int = Path(..., description="Order ID"),
    status: OrderStatus = Query(..., description="New order status"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update an order's status.
    
    Args:
        request: FastAPI request object
        order_id: Order ID
        status: New order status
        db: Database session
        
    Returns:
        Updated order
    """
    db_order = await order.update_status(db, order_id=order_id, status=status)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    return await order.get_with_items(db, order_id=order_id)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete order",
    description="Delete an order by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Order not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@rate_limit()
@handle_db_exceptions
async def delete_order(
    request: Request,
    order_id: int = Path(..., description="Order ID"),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete an order.
    
    Args:
        request: FastAPI request object
        order_id: Order ID
        db: Database session
    """
    db_order = await order.get(db, id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    await order.remove(db, id=order_id)
