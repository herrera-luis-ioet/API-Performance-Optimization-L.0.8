"""Main module for AWS Lambda handler.

This module imports and re-exports the handler from app.main to fix the Lambda import error.
It also ensures that the correct version of asyncio is used.
"""

# Ensure we're using the standard library asyncio
import sys
import asyncio
if hasattr(asyncio.tasks, 'async'):
    # Rename the 'async' function to 'ensure_future' to avoid syntax error
    # This is needed for compatibility with Python 3.7+ where 'async' is a keyword
    asyncio.tasks.ensure_future = asyncio.tasks.async
    del asyncio.tasks.async

from app.main import handler

# Re-export the handler for AWS Lambda
__all__ = ["handler"]
