# Personal Task Manager

A simple, personal task manager application with a three-tier architecture:
- Frontend (Python-based UI)
- API Layer (Python FastAPI)
- Database (PostgreSQL running in a container using Podman)

## Project Structure

```
taskmgr/
├── src/
│   ├── api/         # API layer with FastAPI
│   │   └── tests/   # API tests
│   ├── db/          # Database models and migrations
│   │   └── tests/   # Database tests
│   └── frontend/    # Frontend application
│       └── tests/   # Frontend tests
└── manage.sh        # Management script for operations
```

## Setup and Installation

This project uses conda for Python environment management. The environment name is the same as the project name.

## Management

All stop, start, and restart operations should take place with the `manage.sh` script.

## Database

PostgreSQL is used for persistence, running in a Podman container.
