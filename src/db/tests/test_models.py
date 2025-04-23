"""
Unit tests for the database models.
"""
import pytest
from datetime import datetime, UTC
from db.models import Task, PriorityLevel

def test_task_model_creation():
    """Test creating a Task model instance."""
    # Create a task with all fields
    now = datetime.now(UTC)
    task = Task(
        id=1,
        title="Test Task",
        description="This is a test task",
        due_date=now,
        priority="High",
        completed=False,
        created_at=now,
        updated_at=now
    )
    
    # Check that the task was created with the correct values
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.due_date == now
    assert task.priority == "High"
    assert task.completed is False
    assert task.created_at == now
    assert task.updated_at == now

def test_task_model_representation():
    """Test the string representation of a Task model."""
    task = Task(
        id=1,
        title="Test Task",
        priority="High",
        completed=False
    )
    
    # Check the string representation
    assert str(task) == "<Task(id=1, title='Test Task', priority=High, completed=False)>"

def test_task_to_dict():
    """Test converting a Task model to a dictionary."""
    # Create a task with all fields
    now = datetime.now(UTC)
    task = Task(
        id=1,
        title="Test Task",
        description="This is a test task",
        due_date=now,
        priority="High",
        completed=False,
        created_at=now,
        updated_at=now
    )
    
    # Convert to dictionary
    task_dict = task.to_dict()
    
    # Check that the dictionary has the correct values
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "This is a test task"
    assert task_dict["due_date"] == now.isoformat()
    assert task_dict["priority"] == "High"
    assert task_dict["completed"] is False
    assert task_dict["created_at"] == now.isoformat()
    assert task_dict["updated_at"] == now.isoformat()

def test_task_model_minimal():
    """Test creating a Task model with minimal fields."""
    # Create a task with only required fields
    task = Task(
        title="Minimal Task",
        completed=False  # We need to explicitly set this since SQLAlchemy doesn't apply defaults until flush
    )
    
    # Check that the task was created with the correct values
    assert task.title == "Minimal Task"
    assert task.description is None
    assert task.due_date is None
    assert task.priority is None
    assert task.completed is False
