# API Service Component

A high-performance, scalable FastAPI-based API service component with Redis caching and MySQL database integration.

## Core Technologies

- **Programming Language**: Python 3.9+
- **Web Framework**: FastAPI
- **Database**: MySQL (Amazon RDS)
- **Caching**: Redis
- **Containerization**: Docker
- **Runtime Environment**: Python async runtime

## Build and Development Tools

- **Dependency Management**: Poetry
- **Development Environment**: VSCode
- **Version Control**: Git
- **Testing Frameworks**: 
  * pytest
  * coverage.py
  * locust
- **CI/CD**: GitHub Actions
- **Deployment**: Docker, Kubernetes

## Component Responsibilities

- Implement CRUD operations for products and orders
- Manage Redis-based caching strategies
- Implement distributed rate-limiting
- Handle database interactions with Amazon RDS MySQL
- Provide high-performance, scalable RESTful API endpoints

## Project Structure

```
/
├── app/                            # Main application package
│   ├── __init__.py                 # Package initializer
│   ├── main.py                     # Application entry point
│   ├── api/                        # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py                 # Dependency injection
│   │   └── v1/                     # API version 1
│   │       ├── __init__.py
│   │       ├── api.py              # API router
│   │       └── endpoints/          # API endpoint modules
│   │           ├── __init__.py
│   │           ├── products.py     # Product endpoints
│   │           └── orders.py       # Order endpoints
│   ├── core/                       # Core application modules
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration settings
│   │   ├── cache.py                # Redis cache implementation
│   │   └── rate_limit.py           # Rate limiting implementation
│   ├── crud/                       # CRUD operations
│   │   ├── __init__.py
│   │   ├── base.py                 # Base CRUD class
│   │   ├── product.py              # Product CRUD operations
│   │   └── order.py                # Order CRUD operations
│   ├── db/                         # Database
│   │   ├── __init__.py
│   │   ├── base.py                 # Base database model
│   │   └── session.py              # Database session
│   ├── models/                     # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── product.py              # Product model
│   │   └── order.py                # Order model
│   └── schemas/                    # Pydantic schemas
│       ├── __init__.py
│       ├── product.py              # Product schemas
│       └── order.py                # Order schemas
├── tests/                          # Test directory
│   ├── __init__.py
│   ├── conftest.py                 # Test configuration
│   └── api/                        # API tests
│       ├── __init__.py
│       ├── test_products.py        # Product endpoint tests
│       └── test_orders.py          # Order endpoint tests
├── .github/                        # GitHub configuration
│   └── workflows/                  # GitHub Actions workflows
│       ├── ci.yml                  # CI workflow
│       └── cd.yml                  # CD workflow
├── pyproject.toml                  # Poetry configuration
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
├── .dockerignore                   # Docker ignore file
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

## Setup and Installation

1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository and install dependencies:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the development server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

5. Run with Docker:
   ```bash
   # For development environment
   ./docker-scripts.sh dev-up
   
   # For production environment
   ./docker-scripts.sh prod-up
   ```

## Docker Setup

The project includes Docker configuration for both development and production environments:

### Docker Files
- `Dockerfile`: Multi-stage Docker configuration for development and production
- `docker-compose.yml`: Base Docker Compose configuration with API, Redis, and MySQL services
- `docker-compose.dev.yml`: Development environment overrides
- `docker-compose.prod.yml`: Production environment overrides
- `.dockerignore`: Excludes unnecessary files from Docker build context
- `docker-scripts.sh`: Helper script for Docker operations

### Environment Variables
Environment variables are used for configuration. Copy the example file and modify as needed:
```bash
cp .env.example .env
```

### Docker Commands
The `docker-scripts.sh` script provides convenient commands:

```bash
# Start development environment
./docker-scripts.sh dev-up

# Stop development environment
./docker-scripts.sh dev-down

# Start production environment
./docker-scripts.sh prod-up

# Stop production environment
./docker-scripts.sh prod-down

# Build Docker images
./docker-scripts.sh build

# Show logs from containers
./docker-scripts.sh logs

# Execute command in API container
./docker-scripts.sh exec <command>

# Run tests in Docker container
./docker-scripts.sh test

# Clean Docker resources
./docker-scripts.sh clean
```

### Docker Volumes
The Docker Compose configuration includes persistent volumes for:
- MySQL data: `mysql-data`
- Redis data: `redis-data`

## Development Workflow

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run tests: `poetry run pytest`
4. Submit a pull request

## API Documentation

When the server is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## AWS Lambda Deployment

This API can be deployed to AWS Lambda using AWS CLI through GitHub Actions. The deployment is automated and triggered by version tags. The deployment process packages the application and its dependencies into a ZIP file, uploads it to S3, and updates the Lambda function.

### Deployment Triggers

The Lambda deployment is triggered by version tags with the following format:
- `v{major}.{minor}.{patch}` - Deploys to production (e.g., v1.2.3)

### Prerequisites

1. AWS credentials and configuration in GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`: AWS access key for deployment
   - `AWS_SECRET_ACCESS_KEY`: AWS secret key for deployment
   - `AWS_REGION`: Target AWS region
   - `AWS_S3_BUCKET`: S3 bucket for deployment packages
   - `AWS_LAMBDA_FUNCTION_NAME`: Name of the target Lambda function

2. For local deployment, install required tools:
   ```bash
   # Install AWS CLI
   pip install awscli

   # Configure AWS credentials
   aws configure
   ```

### AWS Configuration

Before deployment, ensure the following AWS resources are configured:

1. VPC with at least two subnets in different availability zones
2. Security Group for Lambda function with required access rules:
   - Outbound access to RDS MySQL (3306)
   - Outbound access to ElastiCache Redis (6379)
   - Outbound access to internet via NAT Gateway
3. Amazon RDS MySQL instance in the VPC
4. Amazon ElastiCache Redis cluster in the VPC
5. S3 bucket for deployment packages
6. Lambda function with appropriate IAM role and permissions:
   - Access to S3 bucket
   - Access to Parameter Store values
   - Connect to RDS
   - Connect to ElastiCache
7. AWS Systems Manager Parameter Store entries:
   ```
   /api-perf/redis/host      # Redis endpoint
   /api-perf/redis/port      # Redis port (default: 6379)
   /api-perf/mysql/host      # RDS endpoint
   /api-perf/mysql/port      # RDS port (default: 3306)
   /api-perf/mysql/user      # Database username
   /api-perf/mysql/password  # Database password
   /api-perf/mysql/database  # Database name
   /api-perf/vpc/security-group-id  # Security group ID
   /api-perf/vpc/subnet-id-1        # First subnet ID
   /api-perf/vpc/subnet-id-2        # Second subnet ID
   ```

### Deployment Methods

#### 1. Automated Deployment (Recommended)

1. Create a new version tag:
   ```bash
   git tag v1.2.3
   ```

2. Push the tag:
   ```bash
   git push origin v1.2.3
   ```

The GitHub Actions workflow will automatically:
- Install dependencies
- Generate deployment package
- Upload package to S3
- Update Lambda function code
- Publish new version

#### 2. Manual Deployment

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies and create deployment package:
   ```bash
   # Install dependencies
   poetry install

   # Export requirements
   poetry export -f requirements.txt --without-hashes > requirements.txt

   # Create deployment package
   mkdir -p deployment-package
   pip install -r requirements.txt --target deployment-package
   cp -r app/* deployment-package/
   cd deployment-package
   zip -r ../lambda-package.zip .
   cd ..
   ```

3. Deploy using AWS CLI:
   ```bash
   # Upload to S3
   aws s3 cp lambda-package.zip s3://your-bucket/deployments/v1.2.3/lambda-package.zip

   # Update Lambda function
   aws lambda update-function-code \
     --function-name your-function-name \
     --s3-bucket your-bucket \
     --s3-key deployments/v1.2.3/lambda-package.zip

   # Update configuration if needed
   aws lambda update-function-configuration \
     --function-name your-function-name \
     --handler app.main.handler \
     --runtime python3.9 \
     --timeout 30 \
     --memory-size 256

   # Publish new version
   aws lambda publish-version \
     --function-name your-function-name \
     --description "Deployment of version v1.2.3"
   ```

### Testing the Deployed API

1. After deployment, get the API endpoint URL from the AWS Console or Lambda function configuration.

2. Test the API using curl or any HTTP client:
   ```bash
   # Get API endpoint from AWS Console
   export API_URL=https://<api-id>.lambda-url.<region>.on.aws

   # Test endpoints
   # Get products
   curl ${API_URL}/products

   # Create a product
   curl -X POST \
     ${API_URL}/products \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Product", "price": 99.99}'

   # Get orders
   curl ${API_URL}/orders

   # Create an order
   curl -X POST \
     ${API_URL}/orders \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1, "quantity": 2}'
   ```

### Configuration and Performance

1. **Lambda Configuration**:
   - Memory: 256MB (configurable via AWS CLI)
   - Timeout: 30 seconds (configurable via AWS CLI)
   - Python Runtime: 3.9
   - VPC: Required for RDS and ElastiCache access
   - Handler: app.main.handler

2. **Cold Start Optimization**:
   - First request may be slower due to cold start
   - Options to minimize impact:
     ```bash
     # Enable Provisioned Concurrency (recommended for production)
     aws lambda put-provisioned-concurrency-config \
       --function-name ${AWS_LAMBDA_FUNCTION_NAME} \
       --provisioned-concurrent-executions 2 \
       --qualifier ${VERSION}
     ```

3. **Monitoring and Logs**:
   ```bash
   # View function logs
   aws logs get-log-events \
     --log-group-name /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME} \
     --log-stream-name $(aws logs describe-log-streams \
       --log-group-name /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME} \
       --order-by LastEventTime \
       --descending \
       --limit 1 \
       --query 'logStreams[0].logStreamName' \
       --output text)

   # Watch logs in real-time
   aws logs tail /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME} --follow

   # Filter logs by time
   aws logs filter-log-events \
     --log-group-name /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME} \
     --start-time $(date -d '5 hours ago' +%s000)

   # Filter logs by pattern
   aws logs filter-log-events \
     --log-group-name /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME} \
     --filter-pattern "Error"
   ```

### Troubleshooting Guide

1. **Deployment Issues**:
   - Check GitHub Actions logs for automated deployments
   - Verify AWS credentials and permissions
   - Ensure S3 bucket exists and is accessible
   - Validate deployment package size (max 50MB compressed)
   - Check Python dependencies in requirements.txt

2. **Runtime Issues**:
   - VPC Configuration:
     - Verify security group rules
     - Check subnet routing tables
     - Ensure NAT Gateway is configured
   - Database Connectivity:
     - Test RDS connection string
     - Verify Redis endpoint is accessible
     - Check security group allows database ports

3. **Performance Issues**:
   - Monitor Lambda metrics in CloudWatch:
     ```bash
     # Get function metrics
     aws cloudwatch get-metric-statistics \
       --namespace AWS/Lambda \
       --metric-name Duration \
       --dimensions Name=FunctionName,Value=${AWS_LAMBDA_FUNCTION_NAME} \
       --start-time $(date -d '1 hour ago' -u +%Y-%m-%dT%H:%M:%SZ) \
       --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
       --period 300 \
       --statistics Average Maximum
     ```
   - Check memory utilization
   - Review execution duration
   - Consider enabling X-Ray tracing

4. **Common Error Solutions**:
   - Timeout errors: Increase Lambda timeout using update-function-configuration
   - Memory errors: Increase Lambda memory allocation
   - Connection errors: Check VPC and security group configuration
   - Cold starts: Enable Provisioned Concurrency

### Cleanup

To remove the deployed Lambda function and associated resources:
```bash
# Delete Lambda function
aws lambda delete-function --function-name ${AWS_LAMBDA_FUNCTION_NAME}

# Delete CloudWatch log group
aws logs delete-log-group \
  --log-group-name /aws/lambda/${AWS_LAMBDA_FUNCTION_NAME}

# Delete deployment packages from S3
aws s3 rm s3://${AWS_S3_BUCKET}/deployments/ --recursive
```

## License

[MIT License](LICENSE)
