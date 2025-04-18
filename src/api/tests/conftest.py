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

# Add the parent directories to the path to import the api and db packages
sys.path.append(str(Path(__file__).parent.parent.parent))

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
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Remove the dependency override
    app.dependency_overrides.clear()
