"""Redis-based rate limiting implementation.

This module provides distributed rate limiting functionality using Redis as the backend.
"""

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import redis.asyncio as redis
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.core.cache import redis_cache
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Rate limit configuration.

    Attributes:
        requests: Maximum number of requests allowed in the period
        period_seconds: Time period in seconds
        prefix: Key prefix for Redis
    """

    requests: int
    period_seconds: int
    prefix: str = "ratelimit"


class RateLimiter:
    """Redis-based distributed rate limiter.

    This class provides rate limiting functionality using Redis as the backend.
    """

    _instance: Optional["RateLimiter"] = None
    _initialized: bool = False

    def __new__(cls) -> "RateLimiter":
        """Create a singleton instance of RateLimiter.

        Returns:
            RateLimiter: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(RateLimiter, cls).__new__(cls)
        return cls._instance

    async def initialize(self) -> None:
        """Initialize the rate limiter.

        This method should be called during application startup.
        """
        if self._initialized:
            return

        try:
            # We use the same Redis client as the cache
            self._initialized = True
            logger.info("Rate limiter initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize rate limiter: {e}")
            raise

    async def close(self) -> None:
        """Close the rate limiter.

        This method should be called during application shutdown.
        """
        self._initialized = False
        logger.info("Rate limiter closed")

    @property
    def client(self) -> redis.Redis:
        """Get the Redis client.

        Returns:
            redis.Redis: Redis client

        Raises:
            RuntimeError: If Redis client is not initialized
        """
        return redis_cache.client

    async def is_rate_limited(
        self, key: str, config: RateLimitConfig
    ) -> Tuple[bool, int, int]:
        """Check if a request is rate limited.

        Args:
            key: Unique identifier for the client
            config: Rate limit configuration

        Returns:
            Tuple containing:
                - bool: True if rate limited, False otherwise
                - int: Number of requests remaining
                - int: Time remaining until reset (seconds)
        """
        if not self._initialized:
            # If not initialized, don't rate limit
            return False, config.requests, config.period_seconds

        try:
            # Use Redis sorted set for rate limiting
            # Each request is a member with score = timestamp
            now = time.time()
            key_name = f"{config.prefix}:{key}"
            
            # Add the current request with the current timestamp
            pipeline = self.client.pipeline()
            pipeline.zadd(key_name, {str(now): now})
            
            # Remove old entries outside the current window
            window_start = now - config.period_seconds
            pipeline.zremrangebyscore(key_name, 0, window_start)
            
            # Count the number of requests in the current window
            pipeline.zcard(key_name)
            
            # Set expiration on the key to auto-cleanup
            pipeline.expire(key_name, config.period_seconds)
            
            # Execute the pipeline
            _, _, request_count, _ = await pipeline.execute()
            
            # Calculate remaining requests and time
            requests_remaining = max(0, config.requests - request_count)
            reset_time = int(config.period_seconds - (now % config.period_seconds))
            
            # Check if rate limited
            is_limited = request_count > config.requests
            
            return is_limited, requests_remaining, reset_time
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            # On error, don't rate limit
            return False, config.requests, config.period_seconds

    def get_client_identifier(self, request: Request) -> str:
        """Generate a unique identifier for the client.

        Args:
            request: FastAPI request object

        Returns:
            str: Unique client identifier
        """
        # Get client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"
        
        # Get user agent
        user_agent = request.headers.get("User-Agent", "")
        
        # Combine IP and user agent for better identification
        identifier = f"{ip}:{user_agent}"
        
        # Hash the identifier for privacy and to keep the key size reasonable
        return hashlib.md5(identifier.encode()).hexdigest()


# Create a global rate limiter instance
rate_limiter = RateLimiter()


# PUBLIC_INTERFACE
def rate_limit(
    requests: Optional[int] = None,
    period_seconds: Optional[int] = None,
    prefix: str = "ratelimit",
) -> Callable:
    """Decorator for rate limiting API endpoints.

    Args:
        requests: Maximum number of requests allowed in the period
        period_seconds: Time period in seconds
        prefix: Key prefix for Redis

    Returns:
        Decorated function
    """
    # Use settings if not specified
    if requests is None:
        requests = settings.RATE_LIMIT_REQUESTS
    if period_seconds is None:
        period_seconds = settings.RATE_LIMIT_PERIOD_SECONDS

    config = RateLimitConfig(
        requests=requests,
        period_seconds=period_seconds,
        prefix=prefix,
    )

    def decorator(func: Callable) -> Callable:
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            # Skip rate limiting if disabled for testing or not initialized
            if RateLimitDependency._testing_disabled or not rate_limiter._initialized:
                return await func(request, *args, **kwargs)
            
            # Get client identifier
            client_id = rate_limiter.get_client_identifier(request)
            
            # Check if rate limited
            is_limited, remaining, reset = await rate_limiter.is_rate_limited(
                client_id, config
            )
            
            # Set rate limit headers
            headers = {
                "X-RateLimit-Limit": str(config.requests),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset),
            }
            
            if is_limited:
                # Return rate limit exceeded response
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded"},
                    headers=headers,
                )
            
            # Execute the function
            response = await func(request, *args, **kwargs)
            
            # Add rate limit headers to the response
            for name, value in headers.items():
                response.headers[name] = value
            
            return response
        
        return wrapper
    
    return decorator


# PUBLIC_INTERFACE
async def get_rate_limiter() -> RateLimiter:
    """Dependency for getting the rate limiter instance.

    Returns:
        RateLimiter: Rate limiter instance
    """
    return rate_limiter


# PUBLIC_INTERFACE
class RateLimitDependency:
    """Rate limit dependency for FastAPI.

    This class provides a dependency that can be used in FastAPI endpoints
    to enforce rate limits.
    """
    
    # Class-level flag to disable rate limiting for testing
    _testing_disabled = False
    
    @classmethod
    def disable_for_testing(cls, disabled: bool = True) -> None:
        """Disable rate limiting for testing purposes.
        
        This method should only be used in tests.
        
        Args:
            disabled: Whether to disable rate limiting
        """
        cls._testing_disabled = disabled

    def __init__(
        self,
        requests: Optional[int] = None,
        period_seconds: Optional[int] = None,
        prefix: str = "ratelimit",
    ):
        """Initialize the rate limit dependency.

        Args:
            requests: Maximum number of requests allowed in the period
            period_seconds: Time period in seconds
            prefix: Key prefix for Redis
        """
        # Use settings if not specified
        self.requests = requests or settings.RATE_LIMIT_REQUESTS
        self.period_seconds = period_seconds or settings.RATE_LIMIT_PERIOD_SECONDS
        self.prefix = prefix
        
        self.config = RateLimitConfig(
            requests=self.requests,
            period_seconds=self.period_seconds,
            prefix=self.prefix,
        )

    async def __call__(self, request: Request) -> None:
        """Check if the request is rate limited.

        Args:
            request: FastAPI request object

        Raises:
            HTTPException: If rate limit is exceeded
        """
        # Skip rate limiting if disabled for testing or not initialized
        if self.__class__._testing_disabled or not rate_limiter._initialized:
            return
        
        # Get client identifier
        client_id = rate_limiter.get_client_identifier(request)
        
        # Check if rate limited
        is_limited, remaining, reset = await rate_limiter.is_rate_limited(
            client_id, self.config
        )
        
        # Set rate limit headers
        headers = {
            "X-RateLimit-Limit": str(self.config.requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset),
        }
        
        if is_limited:
            # Raise rate limit exceeded exception
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers=headers,
            )
