"""
Test script for the Miniban Flask application.
This script tests the task management endpoints using the requests library.
"""

import requests
import subprocess
import time
import signal
import os
import pytest
import sys

# Start the Flask application in the background
def start_flask_app():
    """Start the Flask application in the background."""
    # Add the current directory to Python path so imports work
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    time.sleep(2)  # Wait for the application to start
    return process

# Stop the Flask application
def stop_flask_app(process):
    """Stop the Flask application."""
    os.kill(process.pid, signal.SIGTERM)
    process.wait()

# Test the endpoints
def test_endpoints():
    base_url = "http://localhost:5001"
    
    # Test GET /tasks
    print("Testing GET /tasks")
    response = requests.get(f"{base_url}/tasks")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test POST /tasks
    print("Testing POST /tasks")
    new_task = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "To Do",
        "priority": "High",
        "due_date": "2023-12-31"
    }
    response = requests.post(f"{base_url}/tasks", json=new_task)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test GET /tasks/<id>
    print("Testing GET /tasks/<id>")
    task_id = 1
    response = requests.get(f"{base_url}/tasks/{task_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test PUT /tasks/<id>
    print("Testing PUT /tasks/<id>")
    updated_task = {
        "status": "In Progress"
    }
    response = requests.put(f"{base_url}/tasks/{task_id}", json=updated_task)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test DELETE /tasks/<id>
    print("Testing DELETE /tasks/<id>")
    response = requests.delete(f"{base_url}/tasks/{task_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    # Start the Flask application
    flask_process = start_flask_app()
    
    try:
        # Test the endpoints
        test_endpoints()
    finally:
        # Stop the Flask application
        stop_flask_app(flask_process)

# Pytest fixture for Flask app
@pytest.fixture(scope="module")
def flask_app():
    # Start the Flask application
    flask_process = start_flask_app()
    
    yield flask_process
    
    # Stop the Flask application
    stop_flask_app(flask_process)

# Pytest version of the test
@pytest.mark.usefixtures("flask_app")
def test_endpoints_pytest():
    test_endpoints()

if __name__ == "__main__":
    main()