#!/usr/bin/env python3
"""
Test script for drag-and-drop functionality in the Miniban application.
This script tests the task status update functionality that would be triggered by drag-and-drop.
"""

import requests
import subprocess
import time
import signal
import os
import sys

def start_flask_app():
    """Start the Flask application in the background."""
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    time.sleep(3)  # Wait for the application to start
    return process

def stop_flask_app(process):
    """Stop the Flask application."""
    os.kill(process.pid, signal.SIGTERM)
    process.wait()

def test_drag_drop_functionality():
    """Test the drag-and-drop functionality by simulating status updates."""
    base_url = "http://localhost:5001"
    
    print("=== Testing Drag-and-Drop Functionality ===\n")
    
    # Step 1: Create a test task in "To Do" status
    print("1. Creating a test task...")
    new_task = {
        "title": "Drag and Drop Test Task",
        "description": "This task will be moved between columns",
        "status": "To Do",
        "priority": "Medium",
        "due_date": "2023-12-31"
    }
    
    response = requests.post(f"{base_url}/tasks", json=new_task)
    if response.status_code == 201:
        task = response.json()
        task_id = task['id']
        print(f"✓ Task created successfully with ID: {task_id}")
        print(f"  Initial status: {task['status']}")
    else:
        print(f"✗ Failed to create task: {response.status_code}")
        print(f"  Response: {response.json()}")
        return
    
    # Step 2: Simulate moving task from "To Do" to "In Progress" (drag-and-drop)
    print("\n2. Simulating drag-and-drop: To Do -> In Progress...")
    update_data = {"status": "In Progress"}
    
    response = requests.put(f"{base_url}/tasks/{task_id}", json=update_data)
    if response.status_code == 200:
        updated_task = response.json()
        print(f"✓ Task status updated successfully")
        print(f"  New status: {updated_task['status']}")
    else:
        print(f"✗ Failed to update task status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return
    
    # Step 3: Verify the task is now in "In Progress"
    print("\n3. Verifying task status...")
    response = requests.get(f"{base_url}/tasks/{task_id}")
    if response.status_code == 200:
        task = response.json()
        if task['status'] == "In Progress":
            print(f"✓ Task status verified: {task['status']}")
        else:
            print(f"✗ Task status mismatch. Expected: In Progress, Got: {task['status']}")
    else:
        print(f"✗ Failed to get task: {response.status_code}")
        return
    
    # Step 4: Simulate moving task from "In Progress" to "Done" (drag-and-drop)
    print("\n4. Simulating drag-and-drop: In Progress -> Done...")
    update_data = {"status": "Done"}
    
    response = requests.put(f"{base_url}/tasks/{task_id}", json=update_data)
    if response.status_code == 200:
        updated_task = response.json()
        print(f"✓ Task status updated successfully")
        print(f"  New status: {updated_task['status']}")
    else:
        print(f"✗ Failed to update task status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return
    
    # Step 5: Verify the task is now in "Done"
    print("\n5. Verifying final task status...")
    response = requests.get(f"{base_url}/tasks/{task_id}")
    if response.status_code == 200:
        task = response.json()
        if task['status'] == "Done":
            print(f"✓ Task status verified: {task['status']}")
        else:
            print(f"✗ Task status mismatch. Expected: Done, Got: {task['status']}")
    else:
        print(f"✗ Failed to get task: {response.status_code}")
        return
    
    # Step 6: Test all tasks endpoint to see the task in the correct column
    print("\n6. Verifying task appears in correct column via /tasks endpoint...")
    response = requests.get(f"{base_url}/tasks")
    if response.status_code == 200:
        all_tasks = response.json()
        done_tasks = [t for t in all_tasks if t['status'] == "Done"]
        
        if any(t['id'] == task_id for t in done_tasks):
            print(f"✓ Task {task_id} found in 'Done' column")
        else:
            print(f"✗ Task {task_id} not found in 'Done' column")
    else:
        print(f"✗ Failed to get all tasks: {response.status_code}")
    
    # Step 7: Clean up - delete the test task
    print("\n7. Cleaning up - deleting test task...")
    response = requests.delete(f"{base_url}/tasks/{task_id}")
    if response.status_code == 200:
        print(f"✓ Test task deleted successfully")
    else:
        print(f"✗ Failed to delete task: {response.status_code}")
    
    print("\n=== Drag-and-Drop Test Complete ===")

def main():
    # Start the Flask application
    flask_process = start_flask_app()
    
    try:
        # Test the drag-and-drop functionality
        test_drag_drop_functionality()
    finally:
        # Stop the Flask application
        stop_flask_app(flask_process)

if __name__ == "__main__":
    main()