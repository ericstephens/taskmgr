"""
Repository module for database operations.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Task, PriorityLevel

class TaskRepository:
    """Repository for Task operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.db_session.query(Task).all()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.db_session.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Get tasks by completion status."""
        return self.db_session.query(Task).filter(Task.completed == completed).all()

    def get_tasks_by_priority(self, priority: PriorityLevel) -> List[Task]:
        """Get tasks by priority."""
        return self.db_session.query(Task).filter(Task.priority == priority).all()

    def create_task(self, title: str, description: Optional[str] = None,
                   due_date: Optional[datetime] = None,
                   priority: Optional[PriorityLevel] = None) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            completed=False
        )
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update a task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.db_session.delete(task)
        self.db_session.commit()
        return True

    def mark_task_completed(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed."""
        return self.update_task(task_id, completed=True)

    def mark_task_pending(self, task_id: int) -> Optional[Task]:
        """Mark a task as pending."""
        return self.update_task(task_id, completed=False)
