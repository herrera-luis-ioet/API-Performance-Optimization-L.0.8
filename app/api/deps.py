"""API dependencies.

This module provides dependencies that can be injected into API endpoints.
"""

from typing import AsyncGenerator, Optional, Callable, Dict, Any, List, Type

from fastapi import Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.cache import RedisCache, get_redis_cache
from app.core.rate_limit import RateLimiter, RateLimitDependency, get_rate_limiter
from app.db.session import get_db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session.

    Yields:
        AsyncSession: Database session
    """
    async for session in get_db_session():
        yield session


def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return")
) -> Dict[str, int]:
    """Common pagination parameters.

    Args:
        skip: Number of records to skip
        limit: Max number of records to return

    Returns:
        Dict with pagination parameters
    """
    return {"skip": skip, "limit": limit}


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    detail: str


def handle_db_exceptions(func: Callable) -> Callable:
    """Decorator to handle database exceptions.
    
    Args:
        func: The function to decorate
        
    Returns:
        Decorated function
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log the exception here
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    return wrapper


# PUBLIC_INTERFACE
def get_cache() -> RedisCache:
    """Dependency for getting the Redis cache instance.
    
    Returns:
        RedisCache: Redis cache instance
    """
    return get_redis_cache()


# PUBLIC_INTERFACE
def get_limiter() -> RateLimiter:
    """Dependency for getting the rate limiter instance.
    
    Returns:
        RateLimiter: Rate limiter instance
    """
    return get_rate_limiter()


# PUBLIC_INTERFACE
def rate_limit(
    requests: Optional[int] = None,
    period_seconds: Optional[int] = None,
    prefix: str = "ratelimit",
) -> Callable:
    """Dependency for rate limiting API endpoints.
    
    Args:
        requests: Maximum number of requests allowed in the period
        period_seconds: Time period in seconds
        prefix: Key prefix for Redis
        
    Returns:
        Rate limit dependency
    """
    # Create a RateLimitDependency instance
    dependency = RateLimitDependency(
        requests=requests,
        period_seconds=period_seconds,
        prefix=prefix,
    )
    
    # Return the dependency wrapped in Depends
    return Depends(dependency)
