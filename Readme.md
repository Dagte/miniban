## Description

Miniban is a simple task management application that allows users to create, manage, and organize tasks in a Kanban-style board. It is designed to be ultra-minimalistic and easy to set up and use.

# Run the app:
```
python3 app.py
```

This will start a development server at http://127.0.0.1:5001/.

# Project Structure

```
.
├── app/                  # Main application package
│   ├── __init__.py       # Application factory (create_app())
│   ├── routes.py         # All URL routes and handlers
│   ├── models.py         # Data models and enums
│   ├── dao/              # Data Access Objects
│   │   └── task_dao.py   # Task DAO implementation
│   ├── templates/        # HTML templates
│   │   └── kanban.html   # Kanban board UI
│   └── static/           # Static assets (CSS, JS, images)
├── tests/                # Test files
│   └── test_app.py       # Application tests
├── instance/             # Local data (not committed to git)
│   └── miniban.sqlite    # SQLite database (if used)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── app.py                # Entry point for the application
```

# Features
- Simple and lightweight task management.
- Easy to set up and run.
- Minimalistic design for quick task management.
- RESTful API for task management (CRUD operations).
- Kanban board UI with three columns: To Do, In Progress, Done.
- Task prioritization (High, Medium, Low).
- Due date tracking.
- **Drag-and-drop functionality** to move tasks between columns with automatic status updates.
- Real-time board refresh after task status changes.
- Visual feedback during drag operations.

# Usage

## API Endpoints

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

## Web UI

- **Kanban Board**: Access at http://localhost:5001/kanban
- Displays tasks in three columns based on their status
- Shows task title, description, priority, and due date
- Automatically refreshes to show current task data
- **Drag-and-drop support**: Click and drag tasks between columns to update their status

## Quick Start with Sample Data

Run the test script to populate the board with sample tasks:
```
python test_kanban.py
```

This will:
1. Start the Flask server
2. Create sample tasks with different statuses and priorities
3. Open the Kanban board in your default browser

## Using Drag-and-Drop

The Kanban board now supports intuitive drag-and-drop functionality:

1. **Drag**: Click and hold on any task card
2. **Move**: Drag the task to the desired column (To Do, In Progress, or Done)
3. **Drop**: Release the mouse button to update the task status
4. **Refresh**: The board automatically updates to show the task in its new column

**Example workflow:**
- Drag a task from "To Do" to "In Progress" when you start working on it
- Drag a task from "In Progress" to "Done" when you complete it
- Drag a task back to "To Do" if it needs more work

## Testing Drag-and-Drop

Run the comprehensive test to verify the functionality:
```
python test_drag_drop.py
```

This will:
1. Create a test task
2. Simulate drag-and-drop operations between all columns
3. Verify backend updates
4. Clean up the test task

# Future Plans
- ✅ **COMPLETED**: Add drag-and-drop functionality to move tasks between columns.
- Implement task creation form in the UI.
- Add user authentication and multi-user support.
- Enhance filtering and search capabilities.
- Add touch support for mobile devices.
- Implement undo functionality for accidental drops.

