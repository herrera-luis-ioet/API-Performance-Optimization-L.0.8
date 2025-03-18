"""Main module for AWS Lambda handler.

This module imports and re-exports the handler from app.main to fix the Lambda import error.
"""

from app.main import handler

# Re-export the handler for AWS Lambda
__all__ = ["handler"]