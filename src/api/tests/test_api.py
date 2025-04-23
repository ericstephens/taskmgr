"""
Tests for the Task Manager API endpoints.
"""
import json
from datetime import datetime, timedelta, UTC
import pytest
from fastapi.testclient import TestClient

def test_get_tasks(client):
    """Test getting all tasks."""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    # We should have at least the sample tasks from init.sql
    assert len(tasks) >= 5

def test_get_tasks_filtered_by_completed(client):
    """Test getting tasks filtered by completion status."""
    # Get completed tasks
    response = client.get("/tasks?completed=true")
    assert response.status_code == 200
    completed_tasks = response.json()
    assert isinstance(completed_tasks, list)
    for task in completed_tasks:
        assert task["completed"] is True
    
    # Get pending tasks
    response = client.get("/tasks?completed=false")
    assert response.status_code == 200
    pending_tasks = response.json()
    assert isinstance(pending_tasks, list)
    for task in pending_tasks:
        assert task["completed"] is False

def test_get_task_by_id(client):
    """Test getting a single task by ID."""
    # First get all tasks to get a valid ID
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    
    if tasks:
        task_id = tasks[0]["id"]
        
        # Get the task by ID
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
    
    # Test getting a non-existent task
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_task(client):
    """Test creating a new task."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task created by the API test",
        "due_date": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "priority": "Medium"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["priority"] == task_data["priority"]
    assert created_task["completed"] is False
    
    # Verify the task was actually created
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]

def test_create_task_minimal(client):
    """Test creating a task with minimal data (just title)."""
    task_data = {
        "title": "Minimal Task"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] is None
    assert created_task["due_date"] is None
    assert created_task["priority"] is None
    assert created_task["completed"] is False

def test_update_task(client):
    """Test updating an existing task."""
    # First create a task to update
    task_data = {
        "title": "Task to Update",
        "description": "This task will be updated",
        "priority": "Low"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "This task has been updated",
        "priority": "High"
    }
    
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["priority"] == update_data["priority"]
    
    # Verify the task was actually updated
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

def test_update_task_partial(client):
    """Test partially updating a task."""
    # First create a task to update
    task_data = {
        "title": "Task for Partial Update",
        "description": "This task will be partially updated",
        "priority": "Medium"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    
    # Update only the title
    update_data = {
        "title": "Partially Updated Task"
    }
    
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == task_data["description"]  # Should remain unchanged
    assert updated_task["priority"] == task_data["priority"]  # Should remain unchanged

def test_update_nonexistent_task(client):
    """Test updating a non-existent task."""
    update_data = {
        "title": "Updated Non-existent Task"
    }
    
    response = client.put("/tasks/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(client):
    """Test deleting a task."""
    # First create a task to delete
    task_data = {
        "title": "Task to Delete"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify the task was actually deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_nonexistent_task(client):
    """Test deleting a non-existent task."""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_mark_task_completed(client):
    """Test marking a task as completed."""
    # First create a task
    task_data = {
        "title": "Task to Complete"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    
    # Mark the task as completed
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    
    completed_task = response.json()
    assert completed_task["id"] == task_id
    assert completed_task["completed"] is True
    
    # Verify the task was actually marked as completed
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_mark_nonexistent_task_completed(client):
    """Test marking a non-existent task as completed."""
    response = client.post("/tasks/9999/complete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_mark_task_pending(client):
    """Test marking a task as pending."""
    # First create a task and mark it as completed
    task_data = {
        "title": "Task to Mark as Pending"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    
    # Mark the task as completed
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    
    # Mark the task as pending
    response = client.post(f"/tasks/{task_id}/pending")
    assert response.status_code == 200
    
    pending_task = response.json()
    assert pending_task["id"] == task_id
    assert pending_task["completed"] is False
    
    # Verify the task was actually marked as pending
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is False

def test_mark_nonexistent_task_pending(client):
    """Test marking a non-existent task as pending."""
    response = client.post("/tasks/9999/pending")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
