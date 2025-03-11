"""Mock implementations for rate limiting in tests.

This module provides mock implementations for rate limiting in tests.
"""

from typing import Any, Callable, Optional

from fastapi import Depends, Request

from app.core.rate_limit import RateLimitDependency as BaseRateLimitDependency


class MockRateLimitDependency(BaseRateLimitDependency):
    """Mock implementation of RateLimitDependency for tests.
    
    This class provides a mock implementation of RateLimitDependency that doesn't
    perform any rate limiting.
    """
    
    async def __call__(self, request: Request) -> None:
        """No-op implementation for tests.
        
        Args:
            request: FastAPI request object
        """
        # Do nothing in tests
        return None


def mock_rate_limit(
    requests: Optional[int] = None,
    period_seconds: Optional[int] = None,
    prefix: str = "ratelimit",
) -> Callable:
    """Mock implementation of rate_limit for tests.
    
    Args:
        requests: Maximum number of requests allowed in the period
        period_seconds: Time period in seconds
        prefix: Key prefix for Redis
        
    Returns:
        Mock rate limit dependency
    """
    # Create a MockRateLimitDependency instance
    dependency = MockRateLimitDependency(
        requests=requests,
        period_seconds=period_seconds,
        prefix=prefix,
    )
    
    # Return the dependency wrapped in Depends
    return Depends(dependency)