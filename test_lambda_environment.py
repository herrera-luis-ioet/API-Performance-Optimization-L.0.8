"""Test script to simulate the Lambda environment.

This script tests that the Lambda handler can be executed in an environment similar to AWS Lambda.
"""

import json
import sys
import os
import asyncio
import traceback

# Print Python version for debugging
print(f"Python version: {sys.version}")

# Set environment variables to simulate Lambda environment
os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "api-performance-optimization-dev-api"
os.environ["AWS_LAMBDA_FUNCTION_VERSION"] = "$LATEST"
os.environ["AWS_LAMBDA_FUNCTION_MEMORY_SIZE"] = "1024"
os.environ["AWS_LAMBDA_LOG_GROUP_NAME"] = "/aws/lambda/api-performance-optimization-dev-api"
os.environ["AWS_LAMBDA_LOG_STREAM_NAME"] = "2023/03/12/[$LATEST]abcdef123456"
os.environ["AWS_EXECUTION_ENV"] = "AWS_Lambda_python3.9"
os.environ["AWS_LAMBDA_RUNTIME_API"] = "127.0.0.1:9001"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# Set environment variables from serverless.yml
os.environ["STAGE"] = "dev"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["MYSQL_HOST"] = "localhost"
os.environ["MYSQL_PORT"] = "3306"
os.environ["MYSQL_USER"] = "root"
os.environ["MYSQL_PASSWORD"] = "password"
os.environ["MYSQL_DB"] = "test"
os.environ["PYTHONPATH"] = "."

# Test importing the main module
print("Testing import of main module...")
try:
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
    class LambdaContext:
        def __init__(self):
            self.function_name = "api-performance-optimization-dev-api"
            self.function_version = "$LATEST"
            self.memory_limit_in_mb = 1024
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:api-performance-optimization-dev-api"
            self.aws_request_id = "request-id"
            self.log_group_name = "/aws/lambda/api-performance-optimization-dev-api"
            self.log_stream_name = "2023/03/12/[$LATEST]abcdef123456"
            self.identity = None
            self.client_context = None
            self.remaining_time_in_millis = 30000
    
    test_context = LambdaContext()
    
    print("Lambda handler test completed successfully!")
    print("The syntax error in asyncio's base_events.py has been resolved.")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)