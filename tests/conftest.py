"""Test fixtures for API Performance Optimization.

This module provides fixtures for database and API testing.
"""

import asyncio
import logging
from typing import AsyncGenerator, Dict, Generator, List

import pytest
import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.api.deps import get_db
from app.core.config import settings
from app.db.base import Base

# Import all models to ensure they are registered with Base metadata before creating tables
# This is critical for SQLAlchemy to know about all models when creating tables
from app.models import Product, Order, OrderItem, OrderStatus

# Import main application
from app.main import create_application

# Configure logging
logger = logging.getLogger(__name__)


# Override settings for testing
settings.SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"


# Use the event_loop fixture provided by pytest-asyncio instead of defining our own


@pytest_asyncio.fixture(scope="function")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine."""
    # Make sure we're using in-memory SQLite for testing
    settings.SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        poolclass=NullPool,
        echo=False,
    )
    
    # Import all models to ensure they are registered with Base metadata
    # This is critical for SQLAlchemy to know about all models when creating tables
    from app.models.product import Product
    from app.models.order import Order, OrderItem, OrderStatus
    
    # Create tables
    async with engine.begin() as conn:
        # First drop all tables to ensure a clean state
        await conn.run_sync(Base.metadata.drop_all)
        # Then create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Verify that tables were created and log them
        # Use run_sync to properly inspect the tables with SQLAlchemy's inspect
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        logger.info(f"Created tables: {tables}")
        
        # Verify that all expected tables are created
        expected_tables = ["product", "order", "order_item"]
        missing_tables = [table for table in expected_tables if table not in tables]
        if missing_tables:
            logger.error(f"Missing tables: {missing_tables}")
            raise Exception(f"Failed to create tables: {missing_tables}")
        
        # Verify table columns to ensure they match the model definitions
        for table in expected_tables:
            columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns(table))
            column_names = [col["name"] for col in columns]
            logger.info(f"Table {table} columns: {column_names}")
            
            # Check for critical columns based on table
            if table == "order":
                critical_columns = ["id", "total_amount", "status"]
                missing_columns = [col for col in critical_columns if col not in column_names]
                if missing_columns:
                    logger.error(f"Missing critical columns in {table}: {missing_columns}")
                    raise Exception(f"Table {table} is missing critical columns: {missing_columns}")
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create a new connection for each test
    connection = await test_engine.connect()
    
    # Begin a transaction
    transaction = await connection.begin()
    
    # Create a session bound to the connection
    session = AsyncSession(bind=connection, expire_on_commit=False)
    
    # Create tables for this test if they don't exist
    # This ensures tables are available for each test
    async with connection.begin_nested() as nested:
        # Import all models to ensure they are registered with Base metadata
        from app.models.product import Product
        from app.models.order import Order, OrderItem, OrderStatus
        
        # Create tables within the transaction
        await connection.run_sync(Base.metadata.create_all)
        
        # Verify tables exist
        tables = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        logger.info(f"Tables available for test: {tables}")
    
    yield session
    
    # Clean up
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def app(db_session: AsyncSession) -> FastAPI:
    """Create a test FastAPI application."""
    app = create_application()
    
    # Override the get_db dependency
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Mock Redis cache and rate limiter by disabling them
    # This is a simplified approach for testing
    from app.api.deps import get_cache, get_limiter
    from app.core.rate_limit import RateLimitDependency, rate_limiter
    
    # Disable rate limiting for testing
    RateLimitDependency.disable_for_testing(True)
    
    # Set rate limiter as initialized to avoid initialization errors
    rate_limiter._initialized = True
    
    # Override the dependencies for cache and rate limiter
    app.dependency_overrides[get_cache] = lambda: None
    app.dependency_overrides[get_limiter] = lambda: None
    
    return app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Reset the rate limit testing flag after each test
    from app.core.rate_limit import RateLimitDependency
    RateLimitDependency.disable_for_testing(False)


@pytest_asyncio.fixture(scope="function")
async def test_products(db_session: AsyncSession) -> AsyncGenerator[list, None]:
    """Create test products."""
    products = [
        Product(
            name="Test Product 1",
            description="Test description 1",
            sku="TEST-SKU-001",
            image="https://example.com/images/test-product-1.jpg",
            price=99.99,
            stock=100,
            category="Electronics",
            tags="test,product,electronics",
            is_active=True,
        ),
        Product(
            name="Test Product 2",
            description="Test description 2",
            sku="TEST-SKU-002",
            image="https://example.com/images/test-product-2.jpg",
            price=149.99,
            stock=50,
            category="Electronics",
            tags="test,product,electronics",
            is_active=True,
        ),
        Product(
            name="Test Product 3",
            description="Test description 3",
            sku="TEST-SKU-003",
            image=None,  # Testing with null image
            price=199.99,
            stock=25,
            category="Accessories",
            tags="test,product,accessories",
            is_active=False,
        ),
    ]
    
    for product in products:
        db_session.add(product)
    
    await db_session.commit()
    
    # Refresh products to get their IDs
    for product in products:
        await db_session.refresh(product)
    
    yield products
    
    # Clean up is handled by the db_session fixture


@pytest_asyncio.fixture(scope="function")
async def test_orders(db_session: AsyncSession, test_products: list) -> AsyncGenerator[list, None]:
    """Create test orders."""
    orders = [
        Order(
            status=OrderStatus.PENDING,
            total_amount=199.98,
            customer_email="customer1@example.com",
            customer_name="Test Customer 1",
            shipping_address="123 Test St",
            shipping_city="Test City",
            shipping_country="Test Country",
            shipping_postal_code="12345",
            payment_method="credit_card",
            payment_id="test_payment_1",
        ),
        Order(
            status=OrderStatus.PROCESSING,
            total_amount=149.99,
            customer_email="customer2@example.com",
            customer_name="Test Customer 2",
            shipping_address="456 Test Ave",
            shipping_city="Test City",
            shipping_country="Test Country",
            shipping_postal_code="67890",
            payment_method="paypal",
            payment_id="test_payment_2",
        ),
    ]
    
    for order in orders:
        db_session.add(order)
    
    await db_session.commit()
    
    # Refresh orders to get their IDs
    for order in orders:
        await db_session.refresh(order)
    
    # Add order items
    order_items = [
        OrderItem(
            order_id=orders[0].id,
            product_id=test_products[0].id,
            quantity=2,
            price_at_purchase=test_products[0].price,
            product_name=test_products[0].name,
            product_sku=test_products[0].sku,
        ),
        OrderItem(
            order_id=orders[1].id,
            product_id=test_products[1].id,
            quantity=1,
            price_at_purchase=test_products[1].price,
            product_name=test_products[1].name,
            product_sku=test_products[1].sku,
        ),
    ]
    
    for item in order_items:
        db_session.add(item)
    
    await db_session.commit()
    
    yield orders
    
    # Clean up is handled by the db_session fixture
