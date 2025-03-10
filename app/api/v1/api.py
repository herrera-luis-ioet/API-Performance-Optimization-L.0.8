"""API v1 router.

This module defines the main router for API v1 endpoints.
"""

from fastapi import APIRouter

# Create the main API router for version 1
api_router = APIRouter()

# Import and include routers from endpoint modules
# These will be uncommented and used when the endpoint modules are created
# from app.api.v1.endpoints import products, orders
# api_router.include_router(products.router, prefix="/products", tags=["products"])
# api_router.include_router(orders.router, prefix="/orders", tags=["orders"])


@api_router.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "ok"}