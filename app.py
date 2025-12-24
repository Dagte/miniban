from flask import Flask, request, jsonify, render_template
from task_dao import TaskDAO

print("The value of __name__ is:", __name__)

app = Flask(__name__)

# Initialize the TaskDAO
task_dao = TaskDAO()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Retrieve all tasks."""
    tasks = task_dao.get_all_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'To Do')
    priority = data.get('priority', 'Medium')
    due_date = data.get('due_date')
    
    task = task_dao.create_task(title, description, status, priority, due_date)
    return jsonify(task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a specific task by ID."""
    task = task_dao.get_task(task_id)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    data = request.get_json()
    task = task_dao.update_task(task_id, **data)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    if task_dao.delete_task(task_id):
        return jsonify({"message": "Task deleted successfully"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True, port=5001)

