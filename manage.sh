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
        # Frontend start commands will be added later
        ;;
    stop)
        echo "Stopping all services..."
        echo "Stopping frontend UI..."
        # Frontend stop commands will be added later
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
        # Frontend start commands will be added later
        ;;
    ui-stop)
        echo "Stopping frontend UI..."
        # Frontend stop commands will be added later
        ;;
    setup)
        echo "Setting up the environment..."
        check_podman_machine
        
        # Create conda environment
        echo "Creating conda environment 'taskmgr'..."
        conda create -n taskmgr python=3.11 -y
        
        # Install dependencies for each component
        echo "Installing API dependencies..."
        conda run -n taskmgr pip install -r src/api/requirements.txt
        
        echo "Installing DB dependencies..."
        conda run -n taskmgr pip install -r src/db/requirements.txt
        
        echo "Installing frontend dependencies..."
        conda run -n taskmgr pip install -r src/frontend/requirements.txt
        
        # Start the database
        echo "Setting up the database..."
        $0 db-start
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
