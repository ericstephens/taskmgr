"""
Test module for the task repository.
"""
import sys
import os
import pytest
from datetime import datetime, timedelta, UTC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import the db package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.models import Task, PriorityLevel
from db.repository import TaskRepository

# Test database connection
DATABASE_URL = "postgresql://taskmgr:taskmgr_password@localhost:5432/taskmgr_db"

@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

@pytest.fixture
def task_repository(db_session):
    """Create a task repository for testing."""
    return TaskRepository(db_session)

def test_get_all_tasks(task_repository):
    """Test getting all tasks."""
    tasks = task_repository.get_all_tasks()
    assert len(tasks) >= 5  # We should have at least the 5 sample tasks

def test_get_task_by_id(task_repository):
    """Test getting a task by ID."""
    # Get the first task
    tasks = task_repository.get_all_tasks()
    first_task = tasks[0]
    
    # Get the task by ID
    task = task_repository.get_task_by_id(first_task.id)
    
    assert task is not None
    assert task.id == first_task.id
    assert task.title == first_task.title

def test_get_tasks_by_status(task_repository):
    """Test getting tasks by status."""
    # Get completed tasks
    completed_tasks = task_repository.get_tasks_by_status(True)
    
    # Get pending tasks
    pending_tasks = task_repository.get_tasks_by_status(False)
    
    # Check that we have at least one of each
    assert len(completed_tasks) > 0
    assert len(pending_tasks) > 0
    
    # Check that all completed tasks are marked as completed
    for task in completed_tasks:
        assert task.completed is True
    
    # Check that all pending tasks are marked as not completed
    for task in pending_tasks:
        assert task.completed is False

def test_create_task(task_repository):
    """Test creating a new task."""
    # Create a new task
    title = "Test Task"
    description = "This is a test task"
    due_date = datetime.now(UTC) + timedelta(days=1)
    priority = "Medium"
    
    task = task_repository.create_task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority
    )
    
    # Check that the task was created with the correct values
    assert task.id is not None
    assert task.title == title
    assert task.description == description
    # Compare datetime values without timezone info since SQLAlchemy may store as timezone-naive
    assert task.due_date.replace(tzinfo=None) == due_date.replace(tzinfo=None)
    assert task.priority == priority
    assert task.completed is False

def test_update_task(task_repository):
    """Test updating a task."""
    # Create a new task
    task = task_repository.create_task(
        title="Task to Update",
        description="This task will be updated",
        priority="Low"
    )
    
    # Update the task
    new_title = "Updated Task"
    new_description = "This task has been updated"
    new_priority = "High"
    
    updated_task = task_repository.update_task(
        task.id,
        title=new_title,
        description=new_description,
        priority=new_priority
    )
    
    # Check that the task was updated with the correct values
    assert updated_task.id == task.id
    assert updated_task.title == new_title
    assert updated_task.description == new_description
    assert updated_task.priority == new_priority

def test_delete_task(task_repository):
    """Test deleting a task."""
    # Create a new task
    task = task_repository.create_task(
        title="Task to Delete",
        description="This task will be deleted"
    )
    
    # Get the task ID
    task_id = task.id
    
    # Delete the task
    result = task_repository.delete_task(task_id)
    
    # Check that the task was deleted
    assert result is True
    
    # Try to get the deleted task
    deleted_task = task_repository.get_task_by_id(task_id)
    
    # Check that the task no longer exists
    assert deleted_task is None

def test_mark_task_completed(task_repository):
    """Test marking a task as completed."""
    # Create a new task
    task = task_repository.create_task(
        title="Task to Complete",
        description="This task will be marked as completed"
    )
    
    # Mark the task as completed
    completed_task = task_repository.mark_task_completed(task.id)
    
    # Check that the task was marked as completed
    assert completed_task.id == task.id
    assert completed_task.completed is True

def test_mark_task_pending(task_repository):
    """Test marking a task as pending."""
    # Create a new task and mark it as completed
    task = task_repository.create_task(
        title="Task to Mark as Pending",
        description="This task will be marked as pending"
    )
    task_repository.mark_task_completed(task.id)
    
    # Mark the task as pending
    pending_task = task_repository.mark_task_pending(task.id)
    
    # Check that the task was marked as pending
    assert pending_task.id == task.id
    assert pending_task.completed is False
