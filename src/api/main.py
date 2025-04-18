"""
Main FastAPI application for the Task Manager API.
"""
import sys
import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from contextlib import asynccontextmanager

# Add the parent directory to the path to import the db package
sys.path.append(str(Path(__file__).parent.parent))

from db.database import get_db, init_db
from db.repository import TaskRepository
from db.models import Task

# Initialize database on startup using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application."""
    # Startup: initialize the database
    init_db()
    yield
    # Shutdown: cleanup can be done here if needed

# Create FastAPI app with lifespan
app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks in the Task Manager application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request and response
class TaskBase(BaseModel):
    """Base model for Task data."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    priority: Optional[str] = Field(None, description="Task priority (Low, Medium, High)")

class TaskCreate(TaskBase):
    """Model for creating a new Task."""
    pass

class TaskUpdate(BaseModel):
    """Model for updating an existing Task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    priority: Optional[str] = Field(None, description="Task priority (Low, Medium, High)")
    completed: Optional[bool] = Field(None, description="Whether the task is completed")

class TaskResponse(TaskBase):
    """Model for Task response."""
    id: int = Field(..., description="Task ID")
    completed: bool = Field(..., description="Whether the task is completed")
    created_at: datetime = Field(..., description="When the task was created")
    updated_at: datetime = Field(..., description="When the task was last updated")
    
    # Use ConfigDict instead of class Config
    model_config = ConfigDict(from_attributes=True)



# API endpoints
@app.get("/tasks", response_model=List[TaskResponse], tags=["tasks"])
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    db=Depends(get_db)
):
    """
    Get all tasks, optionally filtered by completion status.
    """
    repo = TaskRepository(db)
    if completed is not None:
        tasks = repo.get_tasks_by_status(completed)
    else:
        tasks = repo.get_all_tasks()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def get_task(task_id: int, db=Depends(get_db)):
    """
    Get a single task by ID.
    """
    repo = TaskRepository(db)
    task = repo.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskResponse, status_code=201, tags=["tasks"])
async def create_task(task: TaskCreate, db=Depends(get_db)):
    """
    Create a new task.
    """
    repo = TaskRepository(db)
    return repo.create_task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority
    )

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def update_task(task_id: int, task: TaskUpdate, db=Depends(get_db)):
    """
    Update an existing task.
    """
    repo = TaskRepository(db)
    
    # Convert Pydantic model to dict and remove None values
    update_data = {k: v for k, v in task.model_dump().items() if v is not None}
    
    updated_task = repo.update_task(task_id, **update_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204, tags=["tasks"])
async def delete_task(task_id: int, db=Depends(get_db)):
    """
    Delete a task.
    """
    repo = TaskRepository(db)
    success = repo.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@app.post("/tasks/{task_id}/complete", response_model=TaskResponse, tags=["tasks"])
async def mark_task_completed(task_id: int, db=Depends(get_db)):
    """
    Mark a task as completed.
    """
    repo = TaskRepository(db)
    task = repo.mark_task_completed(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/{task_id}/pending", response_model=TaskResponse, tags=["tasks"])
async def mark_task_pending(task_id: int, db=Depends(get_db)):
    """
    Mark a task as pending.
    """
    repo = TaskRepository(db)
    task = repo.mark_task_pending(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
