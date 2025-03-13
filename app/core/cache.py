"""Redis cache implementation.

This module provides Redis-based caching functionality with proper TTL management
and cache invalidation strategies.
"""

import asyncio
import functools
import hashlib
import inspect
import json
import logging
from datetime import timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union, cast

import redis.asyncio as redis
from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.config import settings
from app.db.base import Base

# Configure logging
logger = logging.getLogger(__name__)

# Type definitions
T = TypeVar("T")
CacheKeyType = Union[str, int, float, bool, Tuple, List, Dict, BaseModel, Enum, Base, None]
CacheKey = str
CacheValue = Union[str, bytes, int, float, bool, Dict[str, Any], List[Any], None]


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling complex types.
    
    This encoder extends the standard JSONEncoder to handle:
    - Decimal objects (converted to float)
    - SQLAlchemy models (using jsonable_encoder)
    - Enum objects (using value attribute)
    - Pydantic models (using model_dump_json)
    - Other objects (converted to string)
    """
    
    def default(self, obj: Any) -> Any:
        """Override the default method to handle non-serializable types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            JSON serializable object
        """
        try:
            if isinstance(obj, Decimal):
                # Convert Decimal to float for JSON serialization
                return float(obj)
            elif isinstance(obj, Base):
                # Handle SQLAlchemy models
                return jsonable_encoder(obj)
            elif isinstance(obj, Enum):
                # Handle Enum types
                return obj.value
            elif isinstance(obj, BaseModel):
                # Handle Pydantic models
                return json.loads(obj.model_dump_json())
            # Add more type handling as needed
            
            # Let the base class handle the rest or raise TypeError
            return super().default(obj)
        except Exception as e:
            # If all else fails, convert to string
            logger.warning(f"Falling back to string representation for {type(obj).__name__}: {e}")
            return str(obj)


class RedisCache:
    """Redis cache manager.

    This class manages Redis connections and provides methods for caching data
    with proper TTL management and cache invalidation.
    """

    _instance: Optional["RedisCache"] = None
    _redis_client: Optional[redis.Redis] = None
    _initialized: bool = False

    def __new__(cls) -> "RedisCache":
        """Create a singleton instance of RedisCache.

        Returns:
            RedisCache: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(RedisCache, cls).__new__(cls)
        return cls._instance

    async def initialize(self) -> None:
        """Initialize the Redis connection pool.

        This method should be called during application startup.
        """
        if self._initialized:
            return

        try:
            logger.info("Initializing Redis connection pool...")
            connection_kwargs = {
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "db": settings.REDIS_DB,
                "decode_responses": True,
                "encoding": "utf-8",
            }

            if settings.REDIS_PASSWORD:
                connection_kwargs["password"] = settings.REDIS_PASSWORD

            self._redis_client = redis.Redis(**connection_kwargs)
            
            # Test connection
            await self._redis_client.ping()
            
            self._initialized = True
            logger.info("Redis connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection: {e}")
            raise

    async def close(self) -> None:
        """Close the Redis connection pool.

        This method should be called during application shutdown.
        """
        if self._redis_client:
            logger.info("Closing Redis connection pool...")
            await self._redis_client.close()
            self._initialized = False
            logger.info("Redis connection pool closed")

    @property
    def client(self) -> redis.Redis:
        """Get the Redis client.

        Returns:
            redis.Redis: Redis client

        Raises:
            RuntimeError: If Redis client is not initialized
        """
        if not self._redis_client or not self._initialized:
            raise RuntimeError("Redis client is not initialized")
        return self._redis_client

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            value = await self.client.get(key)
            if value is None:
                return None
            
            return self._deserialize(value)
        except Exception as e:
            logger.error(f"Error getting value from cache: {e}")
            return None

    async def set(
        self, key: str, value: Any, expire: Optional[int] = None
    ) -> bool:
        """Set a value in the cache with optional expiration.

        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (None for no expiration)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            serialized_value = self._serialize(value)
            if expire is None:
                expire = settings.REDIS_CACHE_EXPIRE_SECONDS
                
            return await self.client.set(key, serialized_value, ex=expire)
        except Exception as e:
            logger.error(f"Error setting value in cache: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return bool(await self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting value from cache: {e}")
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern.

        Args:
            pattern: Key pattern to match (e.g., "user:*")

        Returns:
            int: Number of keys deleted
        """
        try:
            keys = await self.client.keys(pattern)
            if not keys:
                return 0
                
            return await self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Error deleting keys by pattern: {e}")
            return 0

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache.

        Args:
            key: Cache key

        Returns:
            bool: True if key exists, False otherwise
        """
        try:
            return bool(await self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking if key exists: {e}")
            return False

    async def ttl(self, key: str) -> int:
        """Get the remaining time to live for a key.

        Args:
            key: Cache key

        Returns:
            int: TTL in seconds, -1 if no expiration, -2 if key doesn't exist
        """
        try:
            return await self.client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL: {e}")
            return -2

    async def set_ttl(self, key: str, expire: int) -> bool:
        """Set the expiration time for a key.

        Args:
            key: Cache key
            expire: Expiration time in seconds

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return await self.client.expire(key, expire)
        except Exception as e:
            logger.error(f"Error setting TTL: {e}")
            return False

    async def clear_all(self) -> bool:
        """Clear all cache entries.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return await self.client.flushdb()
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    def _serialize(self, value: Any) -> str:
        """Serialize a value for storage in Redis.

        Args:
            value: Value to serialize

        Returns:
            str: Serialized value
            
        Raises:
            Exception: If serialization fails
        """
        try:
            if isinstance(value, (str, int, float, bool)) or value is None:
                return json.dumps(value)
            elif isinstance(value, (dict, list)):
                return json.dumps(value, cls=CustomJSONEncoder)
            elif isinstance(value, BaseModel):
                return value.model_dump_json()
            elif isinstance(value, Enum):
                return json.dumps(value.value)
            elif isinstance(value, Base):
                # Handle SQLAlchemy models by converting to dict using jsonable_encoder
                # and then serializing with our custom encoder
                return json.dumps(jsonable_encoder(value), cls=CustomJSONEncoder)
            else:
                return json.dumps(value, cls=CustomJSONEncoder)
        except TypeError as e:
            logger.error(f"Type error during serialization: {e}")
            logger.error(f"Failed to serialize object of type: {type(value).__name__}")
            raise
        except ValueError as e:
            logger.error(f"Value error during serialization: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error serializing value: {e}")
            raise

    def _deserialize(self, value: str) -> Any:
        """Deserialize a value from Redis.

        Args:
            value: Serialized value

        Returns:
            Any: Deserialized value
        """
        try:
            return json.loads(value)
        except Exception:
            return value


# Create a global Redis cache instance
redis_cache = RedisCache()


def generate_cache_key(
    prefix: str, *args: CacheKeyType, **kwargs: CacheKeyType
) -> str:
    """Generate a cache key from arguments.

    Args:
        prefix: Key prefix
        *args: Positional arguments to include in the key
        **kwargs: Keyword arguments to include in the key

    Returns:
        str: Generated cache key
    """
    key_parts = [prefix]
    
    # Add positional arguments
    for arg in args:
        if isinstance(arg, BaseModel):
            key_parts.append(arg.model_dump_json())
        elif isinstance(arg, Enum):
            key_parts.append(str(arg.value))
        elif isinstance(arg, Base):
            # Handle SQLAlchemy models
            key_parts.append(json.dumps(jsonable_encoder(arg)))
        else:
            key_parts.append(str(arg))
    
    # Add keyword arguments (sorted for consistency)
    for k in sorted(kwargs.keys()):
        v = kwargs[k]
        if isinstance(v, BaseModel):
            key_parts.append(f"{k}:{v.model_dump_json()}")
        elif isinstance(v, Enum):
            key_parts.append(f"{k}:{v.value}")
        elif isinstance(v, Base):
            # Handle SQLAlchemy models
            key_parts.append(f"{k}:{json.dumps(jsonable_encoder(v))}")
        else:
            key_parts.append(f"{k}:{v}")
    
    # Create a hash of the combined key parts
    key_str = ":".join(key_parts)
    return f"{prefix}:{hashlib.md5(key_str.encode()).hexdigest()}"


# PUBLIC_INTERFACE
def cache(
    expire: Optional[int] = None,
    prefix: Optional[str] = None,
    include_query_params: bool = True,
    include_path_params: bool = True,
) -> Callable:
    """Decorator for caching API endpoint responses.

    Args:
        expire: Cache expiration time in seconds (None for default)
        prefix: Cache key prefix (None for function name)
        include_query_params: Whether to include query parameters in the cache key
        include_path_params: Whether to include path parameters in the cache key

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        # Get function signature for better cache key generation
        sig = inspect.signature(func)
        func_prefix = prefix or func.__name__
        
        # Create a properly wrapped function that preserves the signature
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Skip caching if Redis is not initialized
            if not redis_cache._initialized:
                return await func(*args, **kwargs)
            
            # Extract request object if present
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                for arg_name, arg_val in kwargs.items():
                    if isinstance(arg_val, Request):
                        request = arg_val
                        break
            
            # Build cache key components
            key_components = [func_prefix]
            
            # Add path parameters if requested
            if include_path_params and request:
                path_params = request.path_params
                if path_params:
                    for k, v in sorted(path_params.items()):
                        key_components.append(f"{k}:{v}")
            
            # Add query parameters if requested
            if include_query_params and request:
                query_params = dict(request.query_params)
                if query_params:
                    for k, v in sorted(query_params.items()):
                        key_components.append(f"{k}:{v}")
            
            # Generate the final cache key
            cache_key = generate_cache_key(*key_components)
            
            # Try to get from cache first
            cached_result = await redis_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Cache miss, execute the function
            logger.debug(f"Cache miss for key: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Store the result in cache
            await redis_cache.set(cache_key, result, expire)
            
            return result
        
        # Update wrapper signature to match the original function
        # This is crucial for FastAPI's OpenAPI schema generation
        wrapper.__signature__ = sig
        
        return wrapper
    
    return decorator


# PUBLIC_INTERFACE
def invalidate_cache(pattern: str) -> Callable:
    """Decorator for invalidating cache after a function call.

    Args:
        pattern: Cache key pattern to invalidate (e.g., "user:*")

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        # Get function signature
        sig = inspect.signature(func)
        
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Execute the function first
            result = await func(*args, **kwargs)
            
            # Then invalidate the cache
            if redis_cache._initialized:
                deleted = await redis_cache.delete_pattern(pattern)
                logger.debug(f"Invalidated {deleted} cache keys matching pattern: {pattern}")
            
            return result
        
        # Update wrapper signature to match the original function
        # This is crucial for FastAPI's OpenAPI schema generation
        wrapper.__signature__ = sig
        
        return wrapper
    
    return decorator


# PUBLIC_INTERFACE
async def get_redis_cache() -> RedisCache:
    """Dependency for getting the Redis cache instance.

    Returns:
        RedisCache: Redis cache instance
    """
    return redis_cache
