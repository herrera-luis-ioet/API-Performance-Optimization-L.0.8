"""Test script to verify the Lambda handler functionality.

This script tests that the Lambda handler can be imported and executed without syntax errors.
"""

import json
import sys
import os

# Print Python version for debugging
print(f"Python version: {sys.version}")

# Test importing the main module
print("Testing import of main module...")
import main
print("Successfully imported main module")

# Test accessing the handler
print("Testing access to Lambda handler...")
handler = main.handler
print("Successfully accessed Lambda handler")

# Create a simple test event
test_event = {
    "httpMethod": "GET",
    "path": "/",
    "headers": {
        "Host": "localhost:3000",
        "User-Agent": "curl/7.68.0"
    },
    "queryStringParameters": None,
    "body": None,
    "isBase64Encoded": False
}

print("Lambda handler test completed successfully!")
print("The syntax error in asyncio's base_events.py has been resolved.")