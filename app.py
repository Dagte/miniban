# This file is kept for backward compatibility and local development
# The actual app instance is now in app/__init__.py for Gunicorn compatibility

import sys
import os

# Ensure we can import from the app package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✅ Application imported successfully")
except ImportError as e:
    print(f"❌ Failed to import application: {e}")
    print("💡 Please run: python3 -m pip install -r requirements.txt")
    sys.exit(1)

if __name__ == '__main__':
    print("Starting the Flask application...")
    print("🌐 Open http://localhost:5001/kanban in your browser")
    print("📝 Press Ctrl+C to stop the server")
    app.run(debug=True, port=5001)

