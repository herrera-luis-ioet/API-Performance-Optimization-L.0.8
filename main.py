"""Main module for AWS Lambda handler.

This module imports and re-exports the handler from app.main to fix the Lambda import error.
It also ensures that the correct version of asyncio is used by patching the asyncio module
to handle the 'async' function name which conflicts with Python 3.9+ where 'async' is a reserved keyword.
"""

# Ensure we're using the standard library asyncio
import sys
import asyncio

# Fix for asyncio compatibility issue with Python 3.9+
# Use getattr/setattr to avoid directly referencing 'async' as an attribute name
if hasattr(asyncio.tasks, 'async'):
    # Rename the 'async' function to 'ensure_future' to avoid syntax error
    # This is needed for compatibility with Python 3.7+ where 'async' is a reserved keyword
    setattr(asyncio.tasks, 'ensure_future', getattr(asyncio.tasks, 'async'))
    delattr(asyncio.tasks, 'async')

from app.main import handler

# Re-export the handler for AWS Lambda
__all__ = ["handler"]
