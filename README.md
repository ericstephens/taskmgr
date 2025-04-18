# Personal Task Manager

A comprehensive task management application with a three-tier architecture:
- Frontend (React-based UI with Material UI)
- API Layer (Python FastAPI)
- Database (PostgreSQL running in a Podman container)

## Project Structure

```
taskmgr/
├── src/
│   ├── api/                  # API layer with FastAPI
│   │   ├── main.py          # Main FastAPI application
│   │   ├── config.py        # API configuration
│   │   └── tests/           # API tests
│   ├── db/                  # Database layer
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── repository.py    # Repository pattern implementation
│   │   ├── database.py      # Database connection
│   │   ├── podman-compose.yml # Database container config
│   │   └── tests/           # Database tests
│   └── frontend/            # Frontend application
│       └── task-manager-ui/ # React-based UI
└── manage.sh                # Management script for operations
```

## Prerequisites

- [Conda](https://docs.conda.io/en/latest/) for Python environment management
- [Podman](https://podman.io/) for containerization (instead of Docker)
- [Node.js](https://nodejs.org/) (v14 or higher) and npm for the frontend

## Setup and Installation

The project includes a management script that handles all setup and operations. To get started:

1. Clone the repository:
   ```bash
   git clone https://github.com/ericstephens/taskmgr.git
   cd taskmgr
   ```

2. Set up the backend (Python/conda environment and database):
   ```bash
   ./manage.sh setup
   ```

3. Set up the frontend (React application):
   ```bash
   ./manage.sh setup-ui
   ```

## Running the Application

1. Start all services (database, API, and frontend):
   ```bash
   ./manage.sh start
   ```

2. Access the application:
   - Frontend UI: http://localhost:3000
   - API documentation: http://localhost:8000/docs

3. Stop all services:
   ```bash
   ./manage.sh stop
   ```

## Management Commands

The `manage.sh` script provides various commands to manage the application:

- `./manage.sh start` - Start all services
- `./manage.sh stop` - Stop all services
- `./manage.sh restart` - Restart all services
- `./manage.sh db-start` - Start only the database
- `./manage.sh api-start` - Start only the API
- `./manage.sh ui-start` - Start only the frontend UI
- `./manage.sh test` - Run all tests
- `./manage.sh test-db` - Run database tests
- `./manage.sh test-api` - Run API tests
- `./manage.sh test-ui` - Run frontend tests
- `./manage.sh help` - Show all available commands

## Architecture

### Database Layer

- PostgreSQL database running in a Podman container
- SQLAlchemy ORM for database interactions
- Repository pattern for data access
- Tasks table with fields for id, title, description, due_date, priority, completed, created_at, and updated_at

### API Layer

- FastAPI framework for RESTful API endpoints
- Endpoints for CRUD operations on tasks
- Endpoints for marking tasks as completed/pending
- Comprehensive test suite

### Frontend Layer

- React with TypeScript
- Material UI for responsive design
- Task listing with filtering capabilities
- Forms for adding and editing tasks
- Responsive design that works on mobile and desktop
