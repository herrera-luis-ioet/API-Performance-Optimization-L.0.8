"""Product API endpoints.

This module defines the API endpoints for product operations.
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    ErrorResponse, get_db, get_pagination_params, handle_db_exceptions, rate_limit
)
from app.core.cache import cache, invalidate_cache
from app.crud.product import product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

# Create router for product endpoints
router = APIRouter()


@router.get(
    "/",
    response_model=List[ProductRead],
    summary="Get all products",
    description="Retrieve a list of all products with pagination",
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    dependencies=[rate_limit()]
)
@cache(prefix="products_all", expire=300)  # Cache for 5 minutes
@handle_db_exceptions
async def get_products(
    request: Request,
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get all products with pagination.
    
    Args:
        request: FastAPI request object
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of products
    """
    return await product.get_multi(db, skip=pagination["skip"], limit=pagination["limit"])


@router.get(
    "/active",
    response_model=List[ProductRead],
    summary="Get active products",
    description="Retrieve a list of active products with pagination",
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    dependencies=[rate_limit()]
)
@cache(prefix="products_active", expire=300)  # Cache for 5 minutes
@handle_db_exceptions
async def get_active_products(
    request: Request,
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get active products with pagination.
    
    Args:
        request: FastAPI request object
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of active products
    """
    return await product.get_active(db, skip=pagination["skip"], limit=pagination["limit"])


@router.get(
    "/category/{category}",
    response_model=List[ProductRead],
    summary="Get products by category",
    description="Retrieve a list of products by category with pagination",
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    dependencies=[rate_limit()]
)
@cache(prefix="products_category", expire=300)  # Cache for 5 minutes
@handle_db_exceptions
async def get_products_by_category(
    request: Request,
    category: str = Path(..., description="Product category"),
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
) -> Any:
    """Get products by category with pagination.
    
    Args:
        request: FastAPI request object
        category: Product category
        db: Database session
        pagination: Pagination parameters
        
    Returns:
        List of products in the specified category
    """
    return await product.get_by_category(
        db, category=category, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get(
    "/sku/{sku}",
    response_model=ProductRead,
    summary="Get product by SKU",
    description="Retrieve a product by its SKU",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    dependencies=[rate_limit()]
)
@cache(prefix="product_sku", expire=300)  # Cache for 5 minutes
@handle_db_exceptions
async def get_product_by_sku(
    request: Request,
    sku: str = Path(..., description="Product SKU"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a product by its SKU.
    
    Args:
        request: FastAPI request object
        sku: Product SKU
        db: Database session
        
    Returns:
        Product with the specified SKU
    """
    db_product = await product.get_by_sku(db, sku=sku)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU {sku} not found"
        )
    return db_product


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Get product by ID",
    description="Retrieve a product by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    dependencies=[rate_limit()]
)
@cache(prefix="product_id", expire=300)  # Cache for 5 minutes
@handle_db_exceptions
async def get_product(
    request: Request,
    product_id: int = Path(..., description="Product ID"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a product by its ID.
    
    Args:
        request: FastAPI request object
        product_id: Product ID
        db: Database session
        
    Returns:
        Product with the specified ID
    """
    db_product = await product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return db_product


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@invalidate_cache("products_*")  # Invalidate all product list caches
@handle_db_exceptions
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new product.
    
    Args:
        product_in: Product data
        db: Database session
        
    Returns:
        Created product
    """
    # Check if product with same SKU already exists
    existing_product = await product.get_by_sku(db, sku=product_in.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU {product_in.sku} already exists"
        )
    
    return await product.create(db, obj_in=product_in)


@router.put(
    "/{product_id}",
    response_model=ProductRead,
    summary="Update product",
    description="Update a product by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@invalidate_cache("products_*")  # Invalidate all product list caches
@invalidate_cache("product_id:*")  # Invalidate specific product cache
@invalidate_cache("product_sku:*")  # Invalidate product SKU cache
@handle_db_exceptions
async def update_product(
    product_in: ProductUpdate,
    product_id: int = Path(..., description="Product ID"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a product.
    
    Args:
        product_in: Product data to update
        product_id: Product ID
        db: Database session
        
    Returns:
        Updated product
    """
    db_product = await product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    # If SKU is being updated, check if it already exists
    if product_in.sku and product_in.sku != db_product.sku:
        existing_product = await product.get_by_sku(db, sku=product_in.sku)
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU {product_in.sku} already exists"
            )
    
    return await product.update(db, db_obj=db_product, obj_in=product_in)


@router.patch(
    "/{product_id}/stock",
    response_model=ProductRead,
    summary="Update product stock",
    description="Update a product's stock quantity",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        400: {"model": ErrorResponse, "description": "Invalid stock update"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
@invalidate_cache(f"product_id:*")  # Invalidate specific product cache
@handle_db_exceptions
async def update_product_stock(
    product_id: int = Path(..., description="Product ID"),
    quantity_change: int = Query(..., description="Change in stock quantity (positive for increase, negative for decrease)"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a product's stock quantity.
    
    Args:
        product_id: Product ID
        quantity_change: Change in stock quantity
        db: Database session
        
    Returns:
        Updated product
    """
    db_product = await product.update_stock(db, product_id=product_id, quantity_change=quantity_change)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return db_product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        500: {"model": ErrorResponse, "description": "Database error"}
    },
    response_model=None
)
@invalidate_cache("products_*")  # Invalidate all product list caches
@invalidate_cache("product_id:*")  # Invalidate specific product cache
@invalidate_cache("product_sku:*")  # Invalidate product SKU cache
@handle_db_exceptions
async def delete_product(
    product_id: int = Path(..., description="Product ID"),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete a product.
    
    Args:
        product_id: Product ID
        db: Database session
    """
    db_product = await product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    await product.remove(db, id=product_id)
