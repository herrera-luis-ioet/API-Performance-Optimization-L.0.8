"""Tests for the Redis cache implementation.

This module tests the Redis cache functionality, particularly the serialization
and deserialization of different data types including SQLAlchemy models.
"""

import json
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.cache import RedisCache, generate_cache_key
from app.models.product import Product


@pytest.fixture
def mock_redis_client():
    """Create a mock Redis client."""
    client = AsyncMock()
    client.get = AsyncMock()
    client.set = AsyncMock(return_value=True)
    client.delete = AsyncMock(return_value=1)
    client.keys = AsyncMock()
    client.exists = AsyncMock()
    client.ttl = AsyncMock()
    client.expire = AsyncMock()
    client.flushdb = AsyncMock()
    client.ping = AsyncMock()
    return client


@pytest.fixture
def redis_cache(mock_redis_client):
    """Create a RedisCache instance with a mock Redis client."""
    with patch.object(RedisCache, '_redis_client', mock_redis_client):
        cache = RedisCache()
        cache._initialized = True
        yield cache


@pytest.fixture
def sample_product():
    """Create a sample Product instance for testing."""
    product = Product(
        id=1,
        name="Test Product",
        description="This is a test product",
        sku="TEST-SKU-123",
        price=Decimal("99.99"),
        stock_quantity=100,
        category="Test Category",
        tags="test,product",
        is_active=True
    )
    return product


async def test_product_serialization(redis_cache, sample_product, mock_redis_client):
    """Test that Product objects can be properly serialized and stored in Redis cache."""
    # Set up the mock to return a specific value
    mock_redis_client.set.return_value = True
    
    # Try to cache the product
    result = await redis_cache.set("test:product:1", sample_product)
    
    # Verify the result
    assert result is True, "Failed to set product in cache"
    
    # Verify that set was called with the correct arguments
    mock_redis_client.set.assert_called_once()
    
    # Extract the serialized value that was passed to set
    args, kwargs = mock_redis_client.set.call_args
    key, serialized_value = args
    
    # Verify the key
    assert key == "test:product:1"
    
    # Verify that the serialized value is valid JSON
    try:
        deserialized = json.loads(serialized_value)
        assert isinstance(deserialized, dict), "Serialized product should be a dictionary"
        
        # Verify that the deserialized value contains the expected product attributes
        assert deserialized["id"] == 1
        assert deserialized["name"] == "Test Product"
        assert deserialized["sku"] == "TEST-SKU-123"
        assert deserialized["price"] == 99.99  # Decimal is converted to float in JSON
        assert deserialized["stock_quantity"] == 100
        assert deserialized["category"] == "Test Category"
        assert deserialized["is_active"] is True
    except json.JSONDecodeError:
        pytest.fail("Serialized product is not valid JSON")


async def test_generate_cache_key_with_product(sample_product):
    """Test that generate_cache_key works with Product objects."""
    # Generate a cache key with a product
    key = generate_cache_key("test", sample_product)
    
    # Verify that the key is a string and contains the prefix
    assert isinstance(key, str)
    assert key.startswith("test:")
    
    # Generate a key with product as a keyword argument
    key2 = generate_cache_key("test", product=sample_product)
    
    # Verify that the key is a string and contains the prefix
    assert isinstance(key2, str)
    assert key2.startswith("test:")
    
    # Keys should be different when passing as positional vs keyword
    assert key != key2


async def test_cache_get_with_product(redis_cache, sample_product, mock_redis_client):
    """Test retrieving a cached Product object."""
    # First serialize the product
    serialized = redis_cache._serialize(sample_product)
    
    # Set up the mock to return the serialized product
    mock_redis_client.get.return_value = serialized
    
    # Get the product from cache
    cached_value = await redis_cache.get("test:product:1")
    
    # Verify that get was called with the correct key
    mock_redis_client.get.assert_called_once_with("test:product:1")
    
    # Verify that the returned value is a dictionary with the expected attributes
    assert isinstance(cached_value, dict)
    assert cached_value["id"] == 1
    assert cached_value["name"] == "Test Product"
    assert cached_value["sku"] == "TEST-SKU-123"
    assert cached_value["price"] == 99.99  # Decimal is converted to float in JSON