#!/bin/bash

# Helper script for Docker operations

# Function to display help message
show_help() {
    echo "Usage: ./docker-scripts.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev-up        Start development environment"
    echo "  dev-down      Stop development environment"
    echo "  prod-up       Start production environment"
    echo "  prod-down     Stop production environment"
    echo "  build         Build Docker images"
    echo "  logs          Show logs from containers"
    echo "  exec          Execute command in API container"
    echo "  test          Run tests in Docker container"
    echo "  clean         Remove all containers, volumes, and images"
    echo "  help          Show this help message"
}

# Function to start development environment
dev_up() {
    echo "Starting development environment..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    echo "Development environment started. API available at http://localhost:8000"
    echo "API documentation available at http://localhost:8000/docs"
}

# Function to stop development environment
dev_down() {
    echo "Stopping development environment..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
    echo "Development environment stopped."
}

# Function to start production environment
prod_up() {
    echo "Starting production environment..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    echo "Production environment started. API available at http://localhost:8000"
}

# Function to stop production environment
prod_down() {
    echo "Stopping production environment..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
    echo "Production environment stopped."
}

# Function to build Docker images
build() {
    echo "Building Docker images..."
    docker-compose -f docker-compose.yml build
    echo "Docker images built."
}

# Function to show logs
logs() {
    echo "Showing logs from containers..."
    docker-compose logs -f
}

# Function to execute command in API container
exec_command() {
    echo "Executing command in API container..."
    docker-compose exec api "${@:2}"
}

# Function to run tests
run_tests() {
    echo "Running tests in Docker container..."
    docker-compose exec api poetry run pytest "${@:2}"
}

# Function to clean Docker resources
clean() {
    echo "Removing all containers, volumes, and images..."
    docker-compose down -v
    echo "Docker resources cleaned."
}

# Main script logic
case "$1" in
    dev-up)
        dev_up
        ;;
    dev-down)
        dev_down
        ;;
    prod-up)
        prod_up
        ;;
    prod-down)
        prod_down
        ;;
    build)
        build
        ;;
    logs)
        logs
        ;;
    exec)
        exec_command "$@"
        ;;
    test)
        run_tests "$@"
        ;;
    clean)
        clean
        ;;
    help|*)
        show_help
        ;;
esac