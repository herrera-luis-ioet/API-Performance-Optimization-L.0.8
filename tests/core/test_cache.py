"""Tests for the Redis cache implementation.

This module tests the Redis cache functionality, particularly the serialization
and deserialization of different data types including SQLAlchemy models.
"""

import json
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.cache import RedisCache, generate_cache_key, CustomJSONEncoder
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
        stock=100,
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
        assert deserialized["stock"] == 100
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


async def test_decimal_field_serialization(redis_cache, mock_redis_client):
    """Test that Decimal fields are properly serialized and deserialized."""
    # Create a product with various Decimal values to test edge cases
    product_with_decimals = Product(
        id=42,
        name="Decimal Test Product",
        description="Product with various decimal values",
        sku="DECIMAL-TEST-001",
        price=Decimal("1234.56"),  # Standard decimal
        stock=100,
        category="Test",
        is_active=True
    )
    
    # Set up the mock to return True for set operation
    mock_redis_client.set.return_value = True
    
    # Cache the product
    result = await redis_cache.set("test:decimal:product", product_with_decimals)
    assert result is True, "Failed to set product with decimal fields in cache"
    
    # Extract the serialized value
    args, kwargs = mock_redis_client.set.call_args
    key, serialized_value = args
    
    # Verify the key
    assert key == "test:decimal:product"
    
    # Verify that the serialized value is valid JSON and can be deserialized
    try:
        deserialized = json.loads(serialized_value)
        assert isinstance(deserialized, dict), "Serialized product should be a dictionary"
        
        # Verify decimal fields are properly converted to float
        assert deserialized["price"] == 1234.56
        assert isinstance(deserialized["price"], float), "Decimal should be converted to float"
        
        # Test direct serialization with CustomJSONEncoder
        direct_json = json.dumps(product_with_decimals, cls=CustomJSONEncoder)
        direct_deserialized = json.loads(direct_json)
        
        # Verify the direct serialization also works
        assert direct_deserialized["price"] == 1234.56
        assert isinstance(direct_deserialized["price"], float)
        
        # Set up mock for retrieval
        mock_redis_client.get.return_value = serialized_value
        
        # Test retrieval
        retrieved = await redis_cache.get("test:decimal:product")
        assert retrieved["price"] == 1234.56
        assert isinstance(retrieved["price"], float)
        
    except json.JSONDecodeError as e:
        pytest.fail(f"Serialized product with decimal fields is not valid JSON: {e}")


async def test_decimal_edge_cases_serialization(redis_cache, mock_redis_client):
    """Test serialization of Decimal fields with edge cases."""
    # Create a dictionary with various Decimal edge cases
    decimal_edge_cases = {
        "zero": Decimal("0.0"),
        "negative": Decimal("-123.45"),
        "very_large": Decimal("9999999.99"),
        "very_small": Decimal("0.0001"),
        "high_precision": Decimal("123.456789"),
        "scientific_notation": Decimal("1.23E+10"),
        "integer": Decimal("1000")
    }
    
    # Set up the mock to return True for set operation
    mock_redis_client.set.return_value = True
    
    # Cache the dictionary with decimal edge cases
    result = await redis_cache.set("test:decimal:edge_cases", decimal_edge_cases)
    assert result is True, "Failed to set decimal edge cases in cache"
    
    # Extract the serialized value
    args, kwargs = mock_redis_client.set.call_args
    key, serialized_value = args
    
    # Verify the key
    assert key == "test:decimal:edge_cases"
    
    # Verify that the serialized value is valid JSON and can be deserialized
    try:
        deserialized = json.loads(serialized_value)
        assert isinstance(deserialized, dict), "Serialized value should be a dictionary"
        
        # Verify all decimal values are properly converted to float
        assert deserialized["zero"] == 0.0
        assert deserialized["negative"] == -123.45
        assert deserialized["very_large"] == 9999999.99
        assert deserialized["very_small"] == 0.0001
        assert abs(deserialized["high_precision"] - 123.456789) < 0.000001
        assert deserialized["scientific_notation"] == 12300000000.0
        assert deserialized["integer"] == 1000.0
        
        # Verify all values are floats
        for key, value in deserialized.items():
            assert isinstance(value, float), f"Value for {key} should be a float"
        
        # Test direct serialization with CustomJSONEncoder
        direct_json = json.dumps(decimal_edge_cases, cls=CustomJSONEncoder)
        direct_deserialized = json.loads(direct_json)
        
        # Verify the direct serialization also works for all cases
        assert direct_deserialized["zero"] == 0.0
        assert direct_deserialized["negative"] == -123.45
        assert direct_deserialized["very_large"] == 9999999.99
        assert direct_deserialized["very_small"] == 0.0001
        
        # Set up mock for retrieval
        mock_redis_client.get.return_value = serialized_value
        
        # Test retrieval
        retrieved = await redis_cache.get("test:decimal:edge_cases")
        assert retrieved["zero"] == 0.0
        assert retrieved["negative"] == -123.45
        assert retrieved["very_large"] == 9999999.99
        assert retrieved["very_small"] == 0.0001
        
    except json.JSONDecodeError as e:
        pytest.fail(f"Serialized decimal edge cases is not valid JSON: {e}")


def test_custom_json_encoder_with_decimal():
    """Test the CustomJSONEncoder directly with Decimal values."""
    # Test various Decimal values
    test_cases = [
        (Decimal("0.0"), 0.0),
        (Decimal("123.45"), 123.45),
        (Decimal("-123.45"), -123.45),
        (Decimal("9999999.99"), 9999999.99),
        (Decimal("0.0001"), 0.0001),
        (Decimal("123.456789"), 123.456789),
        (Decimal("1.23E+10"), 12300000000.0),
        (Decimal("1000"), 1000.0)
    ]
    
    # Test each case individually
    for decimal_value, expected_float in test_cases:
        # Serialize the Decimal value
        serialized = json.dumps(decimal_value, cls=CustomJSONEncoder)
        # Deserialize and verify
        deserialized = json.loads(serialized)
        assert deserialized == expected_float, f"Failed for {decimal_value}, got {deserialized}"
        assert isinstance(deserialized, float), f"Result should be float, got {type(deserialized)}"
    
    # Test a complex object with nested Decimal values
    complex_object = {
        "simple_decimal": Decimal("123.45"),
        "nested": {
            "decimal_list": [Decimal("1.1"), Decimal("2.2"), Decimal("3.3")],
            "decimal_dict": {"a": Decimal("4.4"), "b": Decimal("5.5")}
        },
        "mixed_list": [Decimal("6.6"), "string", 7, True, None]
    }
    
    # Serialize the complex object
    serialized = json.dumps(complex_object, cls=CustomJSONEncoder)
    
    # Verify it's valid JSON
    try:
        deserialized = json.loads(serialized)
        
        # Verify the structure and values
        assert deserialized["simple_decimal"] == 123.45
        assert isinstance(deserialized["simple_decimal"], float)
        
        assert deserialized["nested"]["decimal_list"] == [1.1, 2.2, 3.3]
        for item in deserialized["nested"]["decimal_list"]:
            assert isinstance(item, float)
            
        assert deserialized["nested"]["decimal_dict"]["a"] == 4.4
        assert deserialized["nested"]["decimal_dict"]["b"] == 5.5
        assert isinstance(deserialized["nested"]["decimal_dict"]["a"], float)
        
        assert deserialized["mixed_list"][0] == 6.6
        assert isinstance(deserialized["mixed_list"][0], float)
        assert deserialized["mixed_list"][1] == "string"
        assert deserialized["mixed_list"][2] == 7
        assert deserialized["mixed_list"][3] is True
        assert deserialized["mixed_list"][4] is None
        
    except json.JSONDecodeError as e:
        pytest.fail(f"Complex object with Decimal values is not valid JSON: {e}")
