"""
Task Data Access Object (DAO) for managing tasks in memory.
This module simulates a database using an in-memory list of tasks.
"""

from app.models import Task, TaskStatus, TaskPriority

class TaskDAO:
    def __init__(self):
        """Initialize the TaskDAO with an empty list of tasks."""
        self.tasks = []
        self.next_id = 1  # Auto-incrementing ID for new tasks

    def _string_to_status(self, status_str):
        """
        Convert a string status to a TaskStatus enum.
        
        Args:
            status_str (str): The status as a string.
            
        Returns:
            TaskStatus: The corresponding TaskStatus enum.
            
        Raises:
            ValueError: If the status string is not valid.
        """
        status_mapping = {
            "To Do": TaskStatus.TO_DO,
            "In Progress": TaskStatus.IN_PROGRESS,
            "Done": TaskStatus.DONE
        }
        
        if status_str in status_mapping:
            return status_mapping[status_str]
        else:
            raise ValueError(f"Invalid status: {status_str}")

    def _string_to_priority(self, priority_str):
        """
        Convert a string priority to a TaskPriority enum.
        
        Args:
            priority_str (str): The priority as a string.
            
        Returns:
            TaskPriority: The corresponding TaskPriority enum.
            
        Raises:
            ValueError: If the priority string is not valid.
        """
        priority_mapping = {
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        if priority_str in priority_mapping:
            return priority_mapping[priority_str]
        else:
            raise ValueError(f"Invalid priority: {priority_str}")

    def create_task(self, title, description="", status="To Do", priority="Medium", due_date=None):
        """
        Create a new task and add it to the in-memory list.
        
        Args:
            title (str): The title of the task.
            description (str, optional): A brief description of the task. Defaults to "".
            status (str or TaskStatus, optional): The current status of the task. Defaults to "To Do".
            priority (str or TaskPriority, optional): The priority level of the task. Defaults to "Medium".
            due_date (str, optional): The due date for the task. Defaults to None.
        
        Returns:
            Task: The newly created task.
        """
        # Convert string status/priority to enum if needed
        if isinstance(status, str):
            status = self._string_to_status(status)
        if isinstance(priority, str):
            priority = self._string_to_priority(priority)
        
        task = Task(self.next_id, title, description, status, priority, due_date)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id):
        """
        Retrieve a task by its ID.
        
        Args:
            task_id (int): The ID of the task to retrieve.
        
        Returns:
            Task: The task with the specified ID, or None if not found.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self):
        """
        Retrieve all tasks.
        
        Returns:
            list: A list of all tasks.
        """
        return [task.to_dict() for task in self.tasks]

    def update_task(self, task_id, **kwargs):
        """
        Update an existing task.
        
        Args:
            task_id (int): The ID of the task to update.
            **kwargs: Keyword arguments representing the fields to update (e.g., title, description, status).
        
        Returns:
            Task: The updated task, or None if the task was not found.
        """
        task = self.get_task(task_id)
        if task:
            # Convert string status/priority to enum if needed
            if 'status' in kwargs and isinstance(kwargs['status'], str):
                kwargs['status'] = self._string_to_status(kwargs['status'])
            if 'priority' in kwargs and isinstance(kwargs['priority'], str):
                kwargs['priority'] = self._string_to_priority(kwargs['priority'])
            
            task.update(**kwargs)
            return task
        return None

    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): The ID of the task to delete.
        
        Returns:
            bool: True if the task was deleted, False otherwise.
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
