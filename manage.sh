#!/bin/bash

# Management script for the Personal Task Manager application

function show_help {
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  db-start    Start only the database container"
    echo "  db-stop     Stop only the database container"
    echo "  db-status   Check database container status"
    echo "  db-logs     View database container logs"
    echo "  db-shell    Open a psql shell to the database"
    echo "  api-start   Start only the API service"
    echo "  api-stop    Stop only the API service"
    echo "  ui-start    Start only the frontend UI"
    echo "  ui-stop     Stop only the frontend UI"
    echo "  setup       Setup the conda environment and initial configuration"
    echo "  setup-ui    Setup the frontend UI dependencies (requires Node.js)"
    echo "  test        Run all tests"
    echo "  test-api    Run API tests"
    echo "  test-db     Run database tests"
    echo "  test-ui     Run frontend UI tests"
    echo "  otel-start  Start the OpenTelemetry collector and Jaeger"
    echo "  otel-stop   Stop the OpenTelemetry collector and Jaeger"
    echo "  help        Show this help message"
}

# Check if Podman machine is running
check_podman_machine() {
    if ! podman machine list | grep -q "Currently running"; then
        echo "Podman machine is not running. Starting it now..."
        podman machine start
    fi
}

# Check if command is provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Process commands
case "$1" in
    start)
        echo "Starting all services..."
        check_podman_machine
        echo "Starting database container..."
        podman-compose -f "$(pwd)/src/db/podman-compose.yml" up -d
        echo "Starting API service..."
        cd src/api && conda run -n taskmgr uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
        cd "$OLDPWD"
        echo "Starting frontend UI..."
        cd src/frontend/task-manager-ui && npm start &
        cd "$OLDPWD"
        ;;
    stop)
        echo "Stopping all services..."
        echo "Stopping frontend UI..."
        pkill -f "node.*start" || echo "No UI service running"
        echo "Stopping API service..."
        pkill -f "uvicorn main:app" || echo "No API service running"
        echo "Stopping database container..."
        podman-compose -f "$(pwd)/src/db/podman-compose.yml" down
        ;;
    restart)
        echo "Restarting all services..."
        $0 stop
        $0 start
        ;;
    db-start)
        echo "Starting database container..."
        check_podman_machine
        podman-compose -f "$(pwd)/src/db/podman-compose.yml" up -d postgres
        ;;
    db-stop)
        echo "Stopping database container..."
        podman-compose -f "$(pwd)/src/db/podman-compose.yml" stop postgres
        ;;
    db-status)
        echo "Database container status:"
        podman ps -a | grep taskmgr-postgres
        ;;
    db-logs)
        echo "Database container logs:"
        podman logs taskmgr-postgres
        ;;
    db-shell)
        echo "Opening psql shell to database..."
        podman exec -it taskmgr-postgres psql -U taskmgr -d taskmgr_db
        ;;
    api-start)
        echo "Starting API service..."
        check_podman_machine
        cd src/api && conda run -n taskmgr uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    api-stop)
        echo "Stopping API service..."
        # Find and kill the uvicorn process
        pkill -f "uvicorn main:app" || echo "No API service running"
        ;;
    ui-start)
        echo "Starting frontend UI..."
        cd src/frontend/task-manager-ui && npm start
        ;;
    ui-stop)
        echo "Stopping frontend UI..."
        pkill -f "node.*start" || echo "No UI service running"
        ;;
    setup)
        echo "Setting up the environment..."
        check_podman_machine
        
        # Create conda environment from environment.yml
        echo "Creating conda environment 'taskmgr' from environment.yml..."
        conda env create -f environment.yml
        
        # Start the database
        echo "Setting up the database..."
        $0 db-start
        
        echo "\nBackend setup complete!"
        echo "To set up the frontend UI, run: ./manage.sh setup-ui"
        ;;
    setup-ui)
        echo "Setting up the frontend UI..."
        
        # Check if Node.js is installed
        if ! command -v node &> /dev/null; then
            echo "Error: Node.js is not installed. Please install Node.js (v14 or higher) and npm."
            echo "Visit https://nodejs.org/ for installation instructions."
            exit 1
        fi
        
        # Check Node.js version
        NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
        if [ "$NODE_VERSION" -lt 14 ]; then
            echo "Error: Node.js version 14 or higher is required. Current version: $(node -v)"
            echo "Please upgrade Node.js and try again."
            exit 1
        fi
        
        echo "Installing frontend dependencies..."
        cd src/frontend/task-manager-ui && npm install
        cd "$OLDPWD"
        
        echo "\nFrontend UI setup complete!"
        echo "To start all services, run: ./manage.sh start"
        ;;
        
    test)
        echo "Running all tests..."
        echo "\n=== Database Tests ==="
        conda run -n taskmgr pytest -v src/db/tests/
        
        echo "\n=== API Tests ==="
        conda run -n taskmgr pytest -v src/api/tests/
        
        echo "\n=== UI Tests ==="
        cd src/frontend/task-manager-ui && npm test -- --watchAll=false
        cd "$OLDPWD"
        ;;
        
    test-db)
        echo "Running database tests..."
        conda run -n taskmgr pytest -v src/db/tests/
        ;;
        
    test-api)
        echo "Running API tests..."
        conda run -n taskmgr pytest -v src/api/tests/
        ;;
        
    test-ui)
        echo "Running UI tests..."
        cd src/frontend/task-manager-ui && npm test -- --watchAll=false
        cd "$OLDPWD"
        ;;
        
    otel-start)
        echo "Starting OpenTelemetry collector and Jaeger..."
        check_podman_machine
        podman-compose -f "$(pwd)/otel-collector.yml" up -d
        echo "OpenTelemetry collector started. Jaeger UI available at: http://localhost:16686"
        ;;
    otel-stop)
        echo "Stopping OpenTelemetry collector and Jaeger..."
        podman-compose -f "$(pwd)/otel-collector.yml" down
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
