"""Tests for product endpoints.

This module contains tests for the product API endpoints.
"""

import pytest
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.product import Product


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient, test_products: list):
    """Test getting all products."""
    response = await client.get(f"{settings.API_V1_STR}/products/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Test Product 1"
    assert data[1]["name"] == "Test Product 2"
    assert data[2]["name"] == "Test Product 3"


@pytest.mark.asyncio
async def test_get_active_products(client: AsyncClient, test_products: list):
    """Test getting active products."""
    response = await client.get(f"{settings.API_V1_STR}/products/active")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Product 1"
    assert data[1]["name"] == "Test Product 2"
    assert all(product["is_active"] for product in data)


@pytest.mark.asyncio
async def test_get_products_by_category(client: AsyncClient, test_products: list):
    """Test getting products by category."""
    response = await client.get(f"{settings.API_V1_STR}/products/category/Electronics")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(product["category"] == "Electronics" for product in data)


@pytest.mark.asyncio
async def test_get_product_by_sku(client: AsyncClient, test_products: list):
    """Test getting a product by SKU."""
    response = await client.get(f"{settings.API_V1_STR}/products/sku/TEST-SKU-001")
    
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "TEST-SKU-001"
    assert data["name"] == "Test Product 1"


@pytest.mark.asyncio
async def test_get_product_by_sku_not_found(client: AsyncClient):
    """Test getting a product by SKU that doesn't exist."""
    response = await client.get(f"{settings.API_V1_STR}/products/sku/NONEXISTENT-SKU")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, test_products: list):
    """Test getting a product by ID."""
    product_id = test_products[0].id
    response = await client.get(f"{settings.API_V1_STR}/products/{product_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product 1"


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(client: AsyncClient):
    """Test getting a product by ID that doesn't exist."""
    response = await client.get(f"{settings.API_V1_STR}/products/9999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    """Test creating a new product."""
    product_data = {
        "name": "New Test Product",
        "description": "New test description",
        "sku": "NEW-TEST-SKU",
        "price": 299.99,
        "stock_quantity": 75,
        "category": "New Category",
        "tags": "new,test,product",
        "is_active": True
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/products/",
        json=product_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["sku"] == product_data["sku"]
    assert Decimal(str(data["price"])) == Decimal(str(product_data["price"]))
    assert data["stock_quantity"] == product_data["stock_quantity"]
    assert data["category"] == product_data["category"]
    assert data["tags"] == product_data["tags"]
    assert data["is_active"] == product_data["is_active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client: AsyncClient, test_products: list):
    """Test creating a product with a duplicate SKU."""
    product_data = {
        "name": "Duplicate SKU Product",
        "description": "This should fail",
        "sku": "TEST-SKU-001",  # Already exists
        "price": 399.99,
        "stock_quantity": 50,
        "category": "Test",
        "tags": "test,duplicate",
        "is_active": True
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/products/",
        json=product_data
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, test_products: list):
    """Test updating a product."""
    product_id = test_products[0].id
    update_data = {
        "name": "Updated Product Name",
        "price": 129.99,
        "stock_quantity": 200
    }
    
    response = await client.put(
        f"{settings.API_V1_STR}/products/{product_id}",
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == update_data["name"]
    assert Decimal(str(data["price"])) == Decimal(str(update_data["price"]))
    assert data["stock_quantity"] == update_data["stock_quantity"]
    # Fields not in update_data should remain unchanged
    assert data["sku"] == test_products[0].sku
    assert data["category"] == test_products[0].category


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient):
    """Test updating a product that doesn't exist."""
    update_data = {
        "name": "This Should Fail",
        "price": 999.99
    }
    
    response = await client.put(
        f"{settings.API_V1_STR}/products/9999",
        json=update_data
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_product_stock(client: AsyncClient, test_products: list):
    """Test updating a product's stock quantity."""
    product_id = test_products[0].id
    initial_stock = test_products[0].stock_quantity
    quantity_change = 50
    
    response = await client.patch(
        f"{settings.API_V1_STR}/products/{product_id}/stock",
        params={"quantity_change": quantity_change}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["stock_quantity"] == initial_stock + quantity_change


@pytest.mark.asyncio
async def test_update_product_stock_negative(client: AsyncClient, test_products: list):
    """Test decreasing a product's stock quantity."""
    product_id = test_products[1].id
    initial_stock = test_products[1].stock_quantity
    quantity_change = -20
    
    response = await client.patch(
        f"{settings.API_V1_STR}/products/{product_id}/stock",
        params={"quantity_change": quantity_change}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["stock_quantity"] == initial_stock + quantity_change


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_products: list, db_session: AsyncSession):
    """Test deleting a product."""
    product_id = test_products[0].id
    
    response = await client.delete(f"{settings.API_V1_STR}/products/{product_id}")
    
    assert response.status_code == 204
    
    # Verify product is deleted from database
    product = await db_session.get(Product, product_id)
    assert product is None


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient):
    """Test deleting a product that doesn't exist."""
    response = await client.delete(f"{settings.API_V1_STR}/products/9999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]