"""Tests for API dependencies.

This module contains tests for the API dependencies.
"""

import pytest
from unittest.mock import patch

from app.api.deps import generate_url, get_base_url


@pytest.mark.parametrize(
    "path,expected_result",
    [
        ("/api/v1/products", "https://8000_172_31_44_95.workspace.develop.kavia.ai/api/v1/products"),
        ("api/v1/orders", "https://8000_172_31_44_95.workspace.develop.kavia.ai/api/v1/orders"),
        ("/users", "https://8000_172_31_44_95.workspace.develop.kavia.ai/users"),
    ],
)
def test_generate_url(path, expected_result):
    """Test the generate_url function."""
    # Test with default settings (HTTPS)
    result = generate_url(path)
    assert result == expected_result


def test_generate_url_with_http():
    """Test the generate_url function with HTTP protocol."""
    # Mock settings to use HTTP instead of HTTPS
    with patch("app.core.config.settings.USE_HTTPS", False):
        result = generate_url("/api/v1/products")
        assert result == "http://8000_172_31_44_95.workspace.develop.kavia.ai/api/v1/products"


def test_get_base_url():
    """Test the get_base_url dependency."""
    # Test with default settings (HTTPS)
    result = get_base_url()
    assert result == "https://8000_172_31_44_95.workspace.develop.kavia.ai"

    # Mock settings to use HTTP instead of HTTPS
    with patch("app.core.config.settings.USE_HTTPS", False):
        result = get_base_url()
        assert result == "http://8000_172_31_44_95.workspace.develop.kavia.ai"