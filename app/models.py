"""
Models for the Miniban application.
This module defines the data structures used in the application.
"""

from enum import Enum

class TaskStatus(Enum):
    """
    Enum representing the possible statuses of a task.
    """
    TO_DO = "To Do"
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TaskPriority(Enum):
    """
    Enum representing the possible priority levels of a task.
    """
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Task:
    """
    Represents a task in the Kanban board.
    
    Attributes:
        id (int): A unique identifier for the task.
        title (str): The title or name of the task.
        description (str): A brief description of the task.
        status (TaskStatus): The current status of the task (e.g., TaskStatus.TO_DO, TaskStatus.IN_PROGRESS, TaskStatus.DONE).
        priority (TaskPriority): The priority level of the task (e.g., TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW).
        due_date (str, optional): The due date for the task.
    """
    
    def __init__(self, id, title, description="", status=TaskStatus.TO_DO, priority=TaskPriority.MEDIUM, due_date=None):
        """
        Initialize a new Task instance.
        
        Args:
            id (int): A unique identifier for the task.
            title (str): The title or name of the task.
            description (str, optional): A brief description of the task. Defaults to "".
            status (TaskStatus, optional): The current status of the task. Defaults to TaskStatus.TO_DO.
            priority (TaskPriority, optional): The priority level of the task. Defaults to TaskPriority.MEDIUM.
            due_date (str, optional): The due date for the task. Defaults to None.
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
    
    def to_dict(self):
        """
        Convert the Task instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value if isinstance(self.status, TaskStatus) else self.status,
            "priority": self.priority.value if isinstance(self.priority, TaskPriority) else self.priority,
            "due_date": self.due_date
        }
    
    def update(self, **kwargs):
        """
        Update the task's properties.
        
        Args:
            **kwargs: Keyword arguments representing the fields to update (e.g., title, description, status).
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
