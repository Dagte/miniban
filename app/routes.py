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
    return jsonify(task), 201

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a specific task by ID."""
    task_dao = current_app.extensions.get('task_dao')
    task = task_dao.get_task(task_id)
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    task_dao = current_app.extensions.get('task_dao')
    data = request.get_json()
    task = task_dao.update_task(task_id, **data)
    if task:
        return jsonify(task)
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

@bp.route('/admin/cleanup-done', methods=['DELETE'])
def cleanup_done_tasks():
    """
    Admin endpoint for cleaning up Done tasks.
    
    Parameters (JSON):
    - ids: List of task IDs to delete (optional)
    - exceptions: List of task IDs to exclude from deletion (optional)
    
    Rules:
    - Exactly one parameter must be provided (ids OR exceptions, not both)
    - If ids is provided: Delete only those specific tasks (must be in Done status)
    - If exceptions is provided: Delete all Done tasks except those in the exceptions list
    - If neither is provided: Delete all Done tasks
    """
    task_dao = current_app.extensions.get('task_dao')
    
    # Get JSON data - if no JSON provided, use empty dict
    data = request.get_json(silent=True) or {}
    
    ids = data.get('ids', [])
    exceptions = data.get('exceptions', [])
    
    # Validate input - exactly one parameter should be provided
    if ids and exceptions:
        return jsonify({
            "error": "Only one parameter allowed: provide either 'ids' OR 'exceptions', not both"
        }), 400
    
    # Get all Done tasks
    all_tasks = task_dao.get_all_tasks()
    done_tasks = [task for task in all_tasks if task['status'] == 'Done']
    
    if not done_tasks:
        return jsonify({
            "message": "No tasks in Done status found",
            "deleted_count": 0
        }), 200
    
    # Determine which tasks to delete
    if ids:
        # Delete only specified IDs (must be in Done status)
        tasks_to_delete = [task for task in done_tasks if task['id'] in ids]
        invalid_ids = [task_id for task_id in ids if task_id not in [t['id'] for t in done_tasks]]
        
        if invalid_ids:
            return jsonify({
                "error": f"Some IDs are not in Done status or don't exist: {invalid_ids}",
                "valid_ids_deleted": [t['id'] for t in tasks_to_delete]
            }), 400
    else:
        # Delete all Done tasks except those in exceptions list
        if exceptions:
            tasks_to_delete = [task for task in done_tasks if task['id'] not in exceptions]
            invalid_exceptions = [exc_id for exc_id in exceptions if exc_id not in [t['id'] for t in done_tasks]]
            
            if invalid_exceptions:
                return jsonify({
                    "warning": f"Some exception IDs are not in Done status or don't exist: {invalid_exceptions}",
                    "tasks_to_be_deleted": len(tasks_to_delete)
                }), 200
        else:
            # Delete all Done tasks
            tasks_to_delete = done_tasks
    
    # Perform the deletions
    deleted_count = 0
    failed_deletions = []
    
    for task in tasks_to_delete:
        if task_dao.delete_task(task['id']):
            deleted_count += 1
        else:
            failed_deletions.append(task['id'])
    
    # Prepare response
    response = {
        "message": "Cleanup completed successfully",
        "deleted_count": deleted_count,
        "total_done_tasks_before_cleanup": len(done_tasks)
    }
    
    if failed_deletions:
        response["failed_deletions"] = failed_deletions
        response["warning"] = f"Failed to delete {len(failed_deletions)} tasks"
    
    if ids:
        response["operation"] = "specific_ids"
        response["ids_processed"] = ids
    elif exceptions:
        response["operation"] = "all_except_exceptions"
        response["exceptions_count"] = len(exceptions)
        response["exceptions"] = exceptions
    else:
        response["operation"] = "all_done_tasks"
    
    return jsonify(response), 200