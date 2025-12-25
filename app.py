# This file is kept for backward compatibility and local development
# The actual app instance is now in app/__init__.py for Gunicorn compatibility

from app import app

if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True, port=5001)

