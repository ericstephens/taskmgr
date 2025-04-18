"""
Unit tests for the TaskRepository class that mock the database session.
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from db.repository import TaskRepository
from db.models import Task

@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    session = MagicMock()
    return session

@pytest.fixture
def task_repository(mock_db_session):
    """Create a task repository with a mock session."""
    return TaskRepository(mock_db_session)

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id=1,
        title="Test Task",
        description="This is a test task",
        due_date=datetime.utcnow(),
        priority="High",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def test_get_all_tasks(task_repository, mock_db_session, sample_task):
    """Test getting all tasks."""
    # Configure the mock to return a list of tasks
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.all.return_value = [sample_task]
    
    # Call the method
    tasks = task_repository.get_all_tasks()
    
    # Assert that the query was called correctly
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.all.assert_called_once()
    
    # Assert that the result is correct
    assert len(tasks) == 1
    assert tasks[0].id == sample_task.id
    assert tasks[0].title == sample_task.title

def test_get_task_by_id(task_repository, mock_db_session, sample_task):
    """Test getting a task by ID."""
    # Configure the mock to return a task
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = sample_task
    
    # Call the method
    task = task_repository.get_task_by_id(1)
    
    # Assert that the query was called correctly
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once()
    mock_filter.first.assert_called_once()
    
    # Assert that the result is correct
    assert task.id == sample_task.id
    assert task.title == sample_task.title

def test_get_tasks_by_status(task_repository, mock_db_session, sample_task):
    """Test getting tasks by status."""
    # Configure the mock to return a list of tasks
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.all.return_value = [sample_task]
    
    # Call the method
    tasks = task_repository.get_tasks_by_status(False)
    
    # Assert that the query was called correctly
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once()
    mock_filter.all.assert_called_once()
    
    # Assert that the result is correct
    assert len(tasks) == 1
    assert tasks[0].id == sample_task.id
    assert tasks[0].title == sample_task.title

def test_create_task(task_repository, mock_db_session):
    """Test creating a task."""
    # Configure the mock to simulate adding a task
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()
    
    # Call the method
    task = task_repository.create_task(
        title="New Task",
        description="This is a new task",
        priority="Medium"
    )
    
    # Assert that the session methods were called correctly
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    
    # Assert that the task was created with the correct values
    assert task.title == "New Task"
    assert task.description == "This is a new task"
    assert task.priority == "Medium"
    assert task.completed is False

def test_update_task(task_repository, mock_db_session, sample_task):
    """Test updating a task."""
    # Configure the mock to return a task and simulate updating it
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()
    
    # Mock the get_task_by_id method to return the sample task
    task_repository.get_task_by_id = MagicMock(return_value=sample_task)
    
    # Call the method
    updated_task = task_repository.update_task(
        1,
        title="Updated Task",
        description="This task has been updated"
    )
    
    # Assert that the methods were called correctly
    task_repository.get_task_by_id.assert_called_once_with(1)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    
    # Assert that the task was updated with the correct values
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "This task has been updated"

def test_update_nonexistent_task(task_repository, mock_db_session):
    """Test updating a non-existent task."""
    # Configure the mock to return None for get_task_by_id
    task_repository.get_task_by_id = MagicMock(return_value=None)
    
    # Call the method
    updated_task = task_repository.update_task(
        999,
        title="Updated Non-existent Task"
    )
    
    # Assert that get_task_by_id was called correctly
    task_repository.get_task_by_id.assert_called_once_with(999)
    
    # Assert that the result is None
    assert updated_task is None

def test_delete_task(task_repository, mock_db_session, sample_task):
    """Test deleting a task."""
    # Configure the mock to return a task and simulate deleting it
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()
    
    # Mock the get_task_by_id method to return the sample task
    task_repository.get_task_by_id = MagicMock(return_value=sample_task)
    
    # Call the method
    result = task_repository.delete_task(1)
    
    # Assert that the methods were called correctly
    task_repository.get_task_by_id.assert_called_once_with(1)
    mock_db_session.delete.assert_called_once_with(sample_task)
    mock_db_session.commit.assert_called_once()
    
    # Assert that the result is True
    assert result is True

def test_delete_nonexistent_task(task_repository, mock_db_session):
    """Test deleting a non-existent task."""
    # Configure the mock to return None for get_task_by_id
    task_repository.get_task_by_id = MagicMock(return_value=None)
    
    # Call the method
    result = task_repository.delete_task(999)
    
    # Assert that get_task_by_id was called correctly
    task_repository.get_task_by_id.assert_called_once_with(999)
    
    # Assert that the result is False
    assert result is False

def test_mark_task_completed(task_repository, mock_db_session):
    """Test marking a task as completed."""
    # Mock the update_task method
    task_repository.update_task = MagicMock()
    
    # Call the method
    task_repository.mark_task_completed(1)
    
    # Assert that update_task was called correctly
    task_repository.update_task.assert_called_once_with(1, completed=True)

def test_mark_task_pending(task_repository, mock_db_session):
    """Test marking a task as pending."""
    # Mock the update_task method
    task_repository.update_task = MagicMock()
    
    # Call the method
    task_repository.mark_task_pending(1)
    
    # Assert that update_task was called correctly
    task_repository.update_task.assert_called_once_with(1, completed=False)
