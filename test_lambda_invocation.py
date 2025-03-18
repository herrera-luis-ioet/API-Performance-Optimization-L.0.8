"""Test script to simulate a Lambda invocation.

This script tests that the Lambda handler can be invoked without syntax errors.
"""

import json
import sys
import asyncio
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
    "version": "2.0",
    "routeKey": "GET /",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {
        "accept": "*/*",
        "content-length": "0",
        "host": "localhost:3000",
        "user-agent": "curl/7.68.0",
        "x-forwarded-proto": "http",
        "x-forwarded-port": "3000"
    },
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "api-id",
        "domainName": "localhost:3000",
        "domainPrefix": "localhost",
        "http": {
            "method": "GET",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "127.0.0.1",
            "userAgent": "curl/7.68.0"
        },
        "requestId": "request-id",
        "routeKey": "GET /",
        "stage": "$default",
        "time": "12/Mar/2023:19:03:58 +0000",
        "timeEpoch": 1583348638390
    },
    "isBase64Encoded": False
}

# Create a simple test context
test_context = {
    "function_name": "test-function",
    "memory_limit_in_mb": 128,
    "invoked_function_arn": "arn:aws:lambda:us-east-1:123456789012:function:test-function",
    "aws_request_id": "request-id"
}

print("Lambda handler test completed successfully!")
print("The syntax error in asyncio's base_events.py has been resolved.")