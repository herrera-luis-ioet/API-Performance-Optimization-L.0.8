"""Example API endpoints demonstrating URL generation.

This module provides example endpoints that demonstrate how to use the URL generation utility.
"""

from typing import Dict

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_base_url, generate_url


# Create router for example endpoints
router = APIRouter()


@router.get(
    "/",
    response_model=Dict[str, str],
    summary="Get example URLs",
    description="Get example URLs with the correct protocol"
)
async def get_example_urls(
    request: Request,
    base_url: str = Depends(get_base_url)
) -> Dict[str, str]:
    """Get example URLs with the correct protocol.
    
    This endpoint demonstrates how to use the URL generation utility
    to generate URLs with the correct protocol (HTTP or HTTPS).
    
    Args:
        request: FastAPI request object
        base_url: Base URL with the correct protocol
        
    Returns:
        Dict with example URLs
    """
    return {
        "base_url": base_url,
        "products_url": generate_url("/api/v1/products"),
        "orders_url": generate_url("/api/v1/orders"),
        "current_url": generate_url(request.url.path)
    }