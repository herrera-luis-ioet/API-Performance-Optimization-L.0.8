"""Main application module.

This module creates and configures the FastAPI application and provides AWS Lambda handler.
"""

import logging
from typing import Any, Dict

import asyncio
from fastapi import FastAPI, Request, status
from mangum import Mangum
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.api import api_router
from app.core.cache import redis_cache
from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.db.session import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application
    """
    # Create FastAPI app with metadata
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    # Add exception handlers
    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions.

        Args:
            request: Request that caused the exception
            exc: HTTP exception

        Returns:
            JSONResponse: Error response
        """
        logger.error(f"HTTP error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle validation exceptions.

        Args:
            request: Request that caused the exception
            exc: Validation exception

        Returns:
            JSONResponse: Error response with validation details
        """
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @application.get("/")
    def root() -> Dict[str, Any]:
        """Root endpoint.

        Returns:
            dict: Basic API information
        """
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "description": settings.DESCRIPTION,
            "docs": "/docs",
        }

    return application


# Create the FastAPI application
app = create_application()

# Create Lambda handler
handler = Mangum(app, lifespan="off")


# Initialize database and Redis on startup
@app.on_event("startup")
async def startup_db_client() -> None:
    """Initialize database and Redis on startup."""
    try:
        # Initialize database
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully.")
        
        # Initialize Redis cache
        logger.info("Initializing Redis cache...")
        await redis_cache.initialize()
        logger.info("Redis cache initialized successfully.")
        
        # Initialize rate limiter
        logger.info("Initializing rate limiter...")
        await rate_limiter.initialize()
        logger.info("Rate limiter initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_clients() -> None:
    """Close database and Redis connections on shutdown."""
    from app.db.session import engine
    
    # Close database connections
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("Database connections closed.")
    
    # Close Redis cache
    logger.info("Closing Redis cache...")
    await redis_cache.close()
    logger.info("Redis cache closed.")
    
    # Close rate limiter
    logger.info("Closing rate limiter...")
    await rate_limiter.close()
    logger.info("Rate limiter closed.")
