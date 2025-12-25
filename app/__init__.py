"""
Application factory for Miniban.
This module creates the Flask application using the factory pattern
and exposes the app instance for Gunicorn/WSGI servers.
"""

import os
import sqlite3
from flask import Flask
from dotenv import load_dotenv
=======


def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Configuration overrides for testing.
        
    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load environment variables
    load_dotenv()
    
    # Configure the app from environment variables
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),  # Use env var or fallback to 'dev'
        DATABASE=os.getenv('DATABASE_URL', 'instance/miniban.sqlite'),  # Use Supabase or fallback to SQLite
        SUPABASE_URL=os.getenv('SUPABASE_URL'),
        SUPABASE_KEY=os.getenv('SUPABASE_KEY'),
    )
    
    # Log configuration for debugging
    print(f"🔑 Using SECRET_KEY: {'custom' if os.getenv('SECRET_KEY') else 'default'}")
    print(f"🗃 Using DATABASE: {'Supabase' if os.getenv('DATABASE_URL') else 'SQLite'}")
    
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
    
    # Initialize the database and task DAO
    from app.dao.database_factory import DatabaseFactory, SQLiteTaskDAO, SupabaseTaskDAO
    
    # Create database connection
    db_connection = DatabaseFactory.create_database()
    
    # Create appropriate TaskDAO based on database type
    if isinstance(db_connection, sqlite3.Connection):
        task_dao = SQLiteTaskDAO(db_connection)
        print("📊 Using SQLite TaskDAO")
    else:
        # Supabase client
        task_dao = SupabaseTaskDAO(db_connection)
        print("📊 Using Supabase TaskDAO")
    
    # Store in app extensions for access in routes
    app.extensions['task_dao'] = task_dao
    app.extensions['db_connection'] = db_connection
    
    return app


# Create the application instance for Gunicorn/WSGI
# This allows Gunicorn to import app:app successfully
app = create_app()