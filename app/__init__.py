"""
Application factory for Miniban.
This module creates the Flask application using the factory pattern
and exposes the app instance for Gunicorn/WSGI servers.
"""

from flask import Flask


def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Configuration overrides for testing.
        
    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',  # Should be overridden in production
        DATABASE='instance/miniban.sqlite',  # SQLite database in instance folder
    )
    
    if test_config is not None:
        # Load test configuration if provided
        app.config.from_mapping(test_config)
    
    # Ensure instance folder exists
    try:
        import os
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Initialize the task DAO and store it in app extensions
    from app.dao.task_dao import TaskDAO
    task_dao = TaskDAO()
    app.extensions['task_dao'] = task_dao
    
    return app


# Create the application instance for Gunicorn/WSGI
# This allows Gunicorn to import app:app successfully
app = create_app()