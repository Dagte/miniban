"""
Database factory for creating the appropriate database backend.
Supports SQLite (default) and Supabase.
"""

import os
import sqlite3
from supabase import create_client, Client
from typing import Union, Optional

class DatabaseFactory:
    """Factory for creating database connections."""
    
    @staticmethod
    def create_database() -> Union[sqlite3.Connection, Client]:
        """
        Create a database connection based on environment configuration.
        
        Returns:
            Union[sqlite3.Connection, Client]: Database connection object
        """
        database_url = os.getenv('DATABASE_URL')
        
        if database_url and database_url.startswith('postgresql://'):
            # Supabase/PostgreSQL connection
            print("🗃 Connecting to Supabase/PostgreSQL...")
            return DatabaseFactory._create_supabase_client(database_url)
        else:
            # SQLite connection (default)
            print("🗃 Connecting to SQLite...")
            return DatabaseFactory._create_sqlite_connection()
    
    @staticmethod
    def _create_supabase_client(database_url: str) -> Client:
        """
        Create a Supabase client from a PostgreSQL connection URL.
        
        Args:
            database_url (str): PostgreSQL connection URL
            
        Returns:
            Client: Supabase client instance
        """
        # Parse the PostgreSQL URL
        # Format: postgresql://username:password@host:port/database
        import re
        
        # Extract components from the URL
        pattern = r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/([^?]+)'
        match = re.match(pattern, database_url)
        
        if not match:
            raise ValueError(f"Invalid DATABASE_URL format: {database_url}")
        
        username, password, host, port, database = match.groups()
        
        # Get Supabase URL and key from environment
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set for Supabase connection")
        
        # Create and return Supabase client
        return create_client(supabase_url, supabase_key)
    
    @staticmethod
    def _create_sqlite_connection() -> sqlite3.Connection:
        """
        Create a SQLite database connection.
        
        Returns:
            sqlite3.Connection: SQLite connection instance
        """
        # Get database path from environment or use default
        db_path = os.getenv('DATABASE', 'instance/miniban.sqlite')
        
        # Ensure instance folder exists
        import os
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # Create and return SQLite connection
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        
        # Initialize database schema if needed
        DatabaseFactory._initialize_sqlite_schema(conn)
        
        return conn
    
    @staticmethod
    def _initialize_sqlite_schema(conn: sqlite3.Connection):
        """
        Initialize SQLite database schema if tables don't exist.
        
        Args:
            conn (sqlite3.Connection): SQLite connection
        """
        cursor = conn.cursor()
        
        # Create tasks table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()


class SupabaseTaskDAO:
    """Task DAO implementation for Supabase."""
    
    def __init__(self, client: Client):
        self.client = client
        self.table_name = 'tasks'
        
        # Ensure table exists
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the tasks table exists in Supabase."""
        # Supabase automatically creates tables, but we can check
        try:
            response = self.client.table(self.table_name).select('*').limit(1).execute()
            # Table exists or will be created on first insert
        except Exception as e:
            print(f"⚠️  Supabase table check failed: {e}")
    
    def create_task(self, title, description="", status="To Do", priority="Medium", due_date=None):
        """Create a new task in Supabase."""
        task_data = {
            'title': title,
            'description': description,
            'status': status,
            'priority': priority,
            'due_date': due_date
        }
        
        response = self.client.table(self.table_name).insert(task_data).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise Exception("Failed to create task in Supabase")
    
    def get_all_tasks(self):
        """Get all tasks from Supabase."""
        response = self.client.table(self.table_name).select('*').execute()
        return response.data or []
    
    # Add other methods as needed...


class SQLiteTaskDAO:
    """Task DAO implementation for SQLite."""
    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    def create_task(self, title, description="", status="To Do", priority="Medium", due_date=None):
        """Create a new task in SQLite."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, status, priority, due_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, status, priority, due_date))
        
        self.conn.commit()
        
        # Return the created task
        task_id = cursor.lastrowid
        return self.get_task(task_id)
    
    def get_task(self, task_id):
        """Get a single task by ID."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_tasks(self):
        """Get all tasks from SQLite."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_task(self, task_id, **kwargs):
        """Update an existing task."""
        if not kwargs:
            return None
        
        cursor = self.conn.cursor()
        
        # Build the update query dynamically
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(task_id)
        
        query = f"UPDATE tasks SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        
        self.conn.commit()
        
        return self.get_task(task_id)
    
    def delete_task(self, task_id):
        """Delete a task."""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        return cursor.rowcount > 0