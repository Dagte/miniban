#!/usr/bin/env python3
"""
Wrapper script to ensure the correct Python interpreter is used.
This avoids issues with different Python versions or missing modules.
"""

import sys
import os

# Ensure we're using Python 3.11+
if sys.version_info < (3, 11):
    print(f"❌ Error: Python {sys.version} is not supported. Please use Python 3.11+")
    sys.exit(1)

print(f"🐍 Using Python {sys.version}")
print(f"📁 Python executable: {sys.executable}")

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the application
try:
    from app import app
    
    print("✅ Application imported successfully")
    print(f"🌐 Starting Miniban on http://localhost:5001")
    print("📝 Press Ctrl+C to stop the server")
    
    # Run the application
    # Disable reloader and use single thread to avoid SQLite threading issues
    # Also set thread_safe_context_manager to False for better compatibility
    app.run(
        debug=True, 
        port=5001, 
        use_reloader=False, 
        threaded=False,
        use_debugger=True
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try installing missing packages with:")
    print("   python3 -m pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)