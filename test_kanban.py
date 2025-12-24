#!/usr/bin/env python3
"""
Test script to populate the Kanban board with sample tasks.
"""

import requests
import subprocess
import time
import signal
import os
import webbrowser
import sys

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
    time.sleep(3)  # Wait for the application to start
    return process

def stop_flask_app(process):
    """Stop the Flask application."""
    os.kill(process.pid, signal.SIGTERM)
    process.wait()

def create_sample_tasks():
    """Create sample tasks for testing the Kanban board."""
    base_url = "http://localhost:5001"
    
    sample_tasks = [
        {
            "title": "Design database schema",
            "description": "Create the database schema for the new user management system",
            "status": "To Do",
            "priority": "High",
            "due_date": "2024-06-30"
        },
        {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication with login/logout functionality",
            "status": "To Do",
            "priority": "High",
            "due_date": "2024-07-15"
        },
        {
            "title": "Create API documentation",
            "description": "Write comprehensive API documentation using Swagger",
            "status": "In Progress",
            "priority": "Medium",
            "due_date": "2024-07-01"
        },
        {
            "title": "Fix login page bug",
            "description": "The login page crashes when submitting empty fields",
            "status": "In Progress",
            "priority": "High",
            "due_date": "2024-06-25"
        },
        {
            "title": "Update dependencies",
            "description": "Review and update all project dependencies to latest versions",
            "status": "Done",
            "priority": "Low",
            "due_date": "2024-06-20"
        },
        {
            "title": "Add task filtering",
            "description": "Implement API endpoint for filtering tasks by status and priority",
            "status": "To Do",
            "priority": "Medium"
        }
    ]
    
    print("Creating sample tasks...")
    for task in sample_tasks:
        response = requests.post(f"{base_url}/tasks", json=task)
        if response.ok:
            print(f"✓ Created task: {task['title']}")
        else:
            print(f"✗ Failed to create task: {task['title']}")
    
    print("\nSample tasks created successfully!")
    return len(sample_tasks)

def main():
    # Start the Flask application
    print("Starting Flask application...")
    flask_process = start_flask_app()
    
    try:
        # Create sample tasks
        task_count = create_sample_tasks()
        
        # Open the Kanban board in the default browser
        print(f"\nOpening Kanban board in browser...")
        webbrowser.open("http://localhost:5001/kanban")
        
        print(f"\n🎉 Kanban board is ready with {task_count} sample tasks!")
        print("Press Ctrl+C in the terminal to stop the server...")
        
        # Keep the server running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        # Stop the Flask application
        stop_flask_app(flask_process)
        print("Server stopped.")

if __name__ == "__main__":
    main()