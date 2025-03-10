"""API dependencies.

This module provides dependencies that can be injected into API endpoints.
"""

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session.

    Yields:
        AsyncSession: Database session
    """
    async for session in get_db_session():
        yield session