"""Tests for order endpoints.

This module contains tests for the order API endpoints.
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.order import Order, OrderStatus


@pytest.mark.asyncio
async def test_get_orders(client: AsyncClient, test_orders: list):
    """Test getting all orders."""
    response = await client.get(f"{settings.API_V1_STR}/orders/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["customer_email"] == "customer1@example.com"
    assert data[1]["customer_email"] == "customer2@example.com"


@pytest.mark.asyncio
async def test_get_orders_by_customer(client: AsyncClient, test_orders: list):
    """Test getting orders by customer."""
    customer_id = 1
    response = await client.get(f"{settings.API_V1_STR}/orders/customer/{customer_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == customer_id
    assert data[0]["customer_email"] == "customer1@example.com"


@pytest.mark.asyncio
async def test_get_orders_by_status(client: AsyncClient, test_orders: list):
    """Test getting orders by status."""
    status = OrderStatus.PENDING
    response = await client.get(f"{settings.API_V1_STR}/orders/status/{status}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == status
    assert data[0]["customer_email"] == "customer1@example.com"


@pytest.mark.asyncio
async def test_get_orders_by_date_range(client: AsyncClient, test_orders: list):
    """Test getting orders by date range."""
    # Use a date range that includes all test orders
    start_date = (datetime.now() - timedelta(days=1)).isoformat()
    end_date = (datetime.now() + timedelta(days=1)).isoformat()
    
    response = await client.get(
        f"{settings.API_V1_STR}/orders/date-range",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_orders_by_date_range_invalid(client: AsyncClient):
    """Test getting orders with invalid date range."""
    # End date before start date
    start_date = (datetime.now() + timedelta(days=1)).isoformat()
    end_date = (datetime.now() - timedelta(days=1)).isoformat()
    
    response = await client.get(
        f"{settings.API_V1_STR}/orders/date-range",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    assert response.status_code == 400
    assert "End date must be after start date" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_order(client: AsyncClient, test_orders: list):
    """Test getting an order by ID."""
    order_id = test_orders[0].id
    response = await client.get(f"{settings.API_V1_STR}/orders/{order_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_email"] == "customer1@example.com"
    assert data["status"] == OrderStatus.PENDING
    
    # Check that order items are included
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2


@pytest.mark.asyncio
async def test_get_order_not_found(client: AsyncClient):
    """Test getting an order that doesn't exist."""
    response = await client.get(f"{settings.API_V1_STR}/orders/9999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, test_products: list):
    """Test creating a new order."""
    order_data = {
        "customer_email": "newcustomer@example.com",
        "customer_name": "New Test Customer",
        "shipping_address": "789 New Address",
        "shipping_city": "New City",
        "shipping_country": "New Country",
        "shipping_postal_code": "54321",
        "payment_method": "credit_card",
        "payment_id": "new_payment_id",
        "notes": "Test order notes",
        "items": [
            {
                "product_id": test_products[0].id,
                "quantity": 3
            },
            {
                "product_id": test_products[1].id,
                "quantity": 1
            }
        ]
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/orders/",
        json=order_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["customer_email"] == order_data["customer_email"]
    assert data["customer_name"] == order_data["customer_name"]
    assert data["shipping_address"] == order_data["shipping_address"]
    assert data["status"] == OrderStatus.PENDING
    
    # Check order items
    assert len(data["items"]) == 2
    assert data["items"][0]["quantity"] == 3
    assert data["items"][1]["quantity"] == 1
    
    # Check that total amount is calculated correctly
    expected_total = (test_products[0].price * 3) + (test_products[1].price * 1)
    assert Decimal(str(data["total_amount"])) == expected_total


@pytest.mark.asyncio
async def test_create_order_no_items(client: AsyncClient):
    """Test creating an order without items."""
    order_data = {
        "customer_email": "nocustomer@example.com",
        "customer_name": "No Items Customer",
        "shipping_address": "No Items Address",
        "items": []  # Empty items list
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/orders/",
        json=order_data
    )
    
    assert response.status_code == 400
    assert "must have at least one item" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_order(client: AsyncClient, test_orders: list):
    """Test updating an order."""
    order_id = test_orders[0].id
    update_data = {
        "status": OrderStatus.PROCESSING,
        "shipping_address": "Updated Address",
        "notes": "Updated notes"
    }
    
    response = await client.put(
        f"{settings.API_V1_STR}/orders/{order_id}",
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == update_data["status"]
    assert data["shipping_address"] == update_data["shipping_address"]
    assert data["notes"] == update_data["notes"]
    # Fields not in update_data should remain unchanged
    assert data["customer_email"] == test_orders[0].customer_email


@pytest.mark.asyncio
async def test_update_order_not_found(client: AsyncClient):
    """Test updating an order that doesn't exist."""
    update_data = {
        "status": OrderStatus.SHIPPED,
        "notes": "This should fail"
    }
    
    response = await client.put(
        f"{settings.API_V1_STR}/orders/9999",
        json=update_data
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_order_status(client: AsyncClient, test_orders: list):
    """Test updating an order's status."""
    order_id = test_orders[0].id
    new_status = OrderStatus.SHIPPED
    
    response = await client.patch(
        f"{settings.API_V1_STR}/orders/{order_id}/status",
        params={"status": new_status}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == new_status


@pytest.mark.asyncio
async def test_update_order_status_not_found(client: AsyncClient):
    """Test updating the status of an order that doesn't exist."""
    response = await client.patch(
        f"{settings.API_V1_STR}/orders/9999/status",
        params={"status": OrderStatus.DELIVERED}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_order(client: AsyncClient, test_orders: list, db_session: AsyncSession):
    """Test deleting an order."""
    order_id = test_orders[0].id
    
    response = await client.delete(f"{settings.API_V1_STR}/orders/{order_id}")
    
    assert response.status_code == 204
    
    # Verify order is deleted from database
    order = await db_session.get(Order, order_id)
    assert order is None


@pytest.mark.asyncio
async def test_delete_order_not_found(client: AsyncClient):
    """Test deleting an order that doesn't exist."""
    response = await client.delete(f"{settings.API_V1_STR}/orders/9999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]