"""
Routes for the Miniban application.
This module defines all the URL routes and their handlers.
"""

from flask import Blueprint, request, jsonify, render_template, current_app

# Create a blueprint for the main application routes
bp = Blueprint('main', __name__)

@bp.route('/')
def hello_world():
    """Simple hello world endpoint."""
    return 'Hello, World!'

@bp.route('/kanban')
def kanban_board():
    """Serve the Kanban board UI."""
    return render_template('kanban.html')

@bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Retrieve all tasks."""
    task_dao = current_app.extensions.get('task_dao')
    tasks = task_dao.get_all_tasks()
    return jsonify(tasks)

@bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    task_dao = current_app.extensions.get('task_dao')
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'To Do')
    priority = data.get('priority', 'Medium')
    due_date = data.get('due_date')
    
    task = task_dao.create_task(title, description, status, priority, due_date)
    return jsonify(task.to_dict()), 201

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a specific task by ID."""
    task_dao = current_app.extensions.get('task_dao')
    task = task_dao.get_task(task_id)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    task_dao = current_app.extensions.get('task_dao')
    data = request.get_json()
    task = task_dao.update_task(task_id, **data)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task_dao = current_app.extensions.get('task_dao')
    if task_dao.delete_task(task_id):
        return jsonify({"message": "Task deleted successfully"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404