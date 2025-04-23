"""
Pytest configuration file for API tests.
"""
import sys
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

# Add the parent directories to the path to import the api and db packages
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import OpenTelemetry configuration
from api.tests.otel_config import setup_tracer, instrument_fastapi, instrument_sqlalchemy, cleanup_tracer

# Set up the tracer
tracer = setup_tracer()

from db.database import Base, get_db
from api.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql://taskmgr:taskmgr_password@localhost:5432/taskmgr_db"

# Create test engine
engine = create_engine(TEST_DATABASE_URL)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create a test database session."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Instrument SQLAlchemy with OpenTelemetry
    instrument_sqlalchemy(engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """Create a test client for the FastAPI app."""
    # Override the get_db dependency to use the test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Instrument FastAPI with OpenTelemetry
    instrument_fastapi(app)
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Remove the dependency override
    app.dependency_overrides.clear()
