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

This API can be deployed to AWS Lambda using the Serverless Framework. The deployment configuration is defined in `serverless.yml`.

### Prerequisites

1. Install the Serverless Framework:
   ```bash
   npm install -g serverless
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Install the Serverless Python Requirements plugin:
   ```bash
   serverless plugin install -n serverless-python-requirements
   ```

### AWS Configuration

Before deployment, ensure the following AWS resources are configured:

1. VPC with at least two subnets
2. Security Group for Lambda function
3. Amazon RDS MySQL instance
4. Amazon ElastiCache Redis cluster
5. AWS Systems Manager Parameter Store entries:
   ```
   /api-perf/${stage}/redis/host
   /api-perf/${stage}/redis/port
   /api-perf/${stage}/mysql/host
   /api-perf/${stage}/mysql/port
   /api-perf/${stage}/mysql/user
   /api-perf/${stage}/mysql/password
   /api-perf/${stage}/mysql/database
   /api-perf/${stage}/vpc/security-group-id
   /api-perf/${stage}/vpc/subnet-id-1
   /api-perf/${stage}/vpc/subnet-id-2
   ```

### Environment Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Deployment Steps

1. Generate requirements.txt from poetry:
   ```bash
   poetry export -f requirements.txt --without-hashes > requirements.txt
   ```

2. Deploy to a specific stage (e.g., dev, staging, prod):
   ```bash
   serverless deploy --stage dev --region us-east-1
   ```

   Or use the default stage (dev):
   ```bash
   serverless deploy
   ```

3. To deploy to a different region:
   ```bash
   serverless deploy --region eu-west-1
   ```

### Testing the Deployed API

1. After deployment, Serverless Framework will output the API endpoint URLs.

2. Test the API using curl or any HTTP client:
   ```bash
   # Get products
   curl https://<api-id>.execute-api.<region>.amazonaws.com/products

   # Create a product (replace with your actual endpoint)
   curl -X POST \
     https://<api-id>.execute-api.<region>.amazonaws.com/products \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Product", "price": 99.99}'
   ```

### Troubleshooting

1. **Cold Start Issues**:
   - The first request might be slower due to Lambda cold start
   - Consider using Provisioned Concurrency for consistent performance

2. **VPC Configuration**:
   - Ensure Lambda has proper VPC access to RDS and ElastiCache
   - Check security group rules allow necessary connections

3. **Memory and Timeout**:
   - Default configuration: 1024MB memory, 30s timeout
   - Adjust in serverless.yml if needed

4. **Logs**:
   - View Lambda logs:
     ```bash
     serverless logs -f api
     ```
   - Stream logs in real-time:
     ```bash
     serverless logs -f api -t
     ```

5. **Common Issues**:
   - Check IAM roles and permissions
   - Verify Parameter Store values are correct
   - Ensure VPC has internet access via NAT Gateway
   - Confirm Python dependencies are properly packaged

### Cleanup

To remove the deployed service and all resources:
```bash
serverless remove --stage <stage-name>
```

## License

[MIT License](LICENSE)
