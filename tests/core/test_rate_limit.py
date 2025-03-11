"""Tests for rate limiting functionality.

This module contains tests for the rate limiting functionality.
"""

import pytest
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from app.core.rate_limit import rate_limit
from app.models.order import Order


@pytest.mark.asyncio
async def test_rate_limit_with_model_object(app: FastAPI, client: AsyncClient):
    """Test rate limit decorator with model object."""
    
    # Create a test endpoint that returns a model object
    @app.get("/test/model-object")
    @rate_limit()
    async def get_model_object(request: Request):
        # Create and return a model object (Order)
        return Order(
            customer_email="test@example.com",
            customer_name="Test Customer"
        )
    
    # Test the endpoint
    response = await client.get("/test/model-object")
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that rate limit headers are present
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers
    
    # Check response content
    data = response.json()
    assert data["customer_email"] == "test@example.com"
    assert data["customer_name"] == "Test Customer"


@pytest.mark.asyncio
async def test_rate_limit_with_response_object(app: FastAPI, client: AsyncClient):
    """Test rate limit decorator with Response object."""
    
    # Create a test endpoint that returns a Response object
    @app.get("/test/response-object")
    @rate_limit()
    async def get_response_object(request: Request):
        # Return a JSONResponse
        return JSONResponse(
            content={"message": "This is a test response"}
        )
    
    # Test the endpoint
    response = await client.get("/test/response-object")
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that rate limit headers are present
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers
    
    # Check response content
    data = response.json()
    assert data["message"] == "This is a test response"