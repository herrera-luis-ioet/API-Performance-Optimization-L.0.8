"""Database session management.

This module provides functionality for managing database sessions and connections
with proper connection pooling and async support for Amazon RDS MySQL.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create async engine with connection pooling
engine = create_async_engine(
    settings.get_database_uri,
    echo=False,  # Set to True for SQL query logging (development only)
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=30,  # Seconds to wait before timing out on getting a connection from the pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
    # Using the default AsyncAdaptedQueuePool which is compatible with asyncio
    # Alternatively, we could use NullPool to disable pooling: poolclass=NullPool
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get a database connection from the pool.

    Yields:
        AsyncConnection: Database connection
    """
    async with engine.begin() as connection:
        yield connection


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session.

    Yields:
        AsyncSession: Database session
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for database sessions.

    Yields:
        AsyncSession: Database session
    """
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        await session.close()


# Function to initialize the database (create tables, etc.)
async def init_db() -> None:
    """Initialize the database.

    Creates all tables defined in the models.
    """
    from app.db.base import Base

    async with engine.begin() as conn:
        # Import all models to ensure they are registered with the Base metadata
        # This is needed for create_all to work properly
        from app.models.product import Product  # noqa
        from app.models.order import Order, OrderItem  # noqa

        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")
