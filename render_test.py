#!/usr/bin/env python3
"""
Test script to verify Render compatibility
"""

def test_render_compatibility():
    """Test that the app is Render-compatible"""
    
    # Test 1: Check that app.py has the app variable
    try:
        import app
        assert hasattr(app, 'app'), "app.py should have 'app' variable"
        print("✅ app.py has 'app' variable")
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return False
    
    # Test 2: Check that requirements.txt has gunicorn
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        assert 'gunicorn' in requirements, "requirements.txt should include gunicorn"
        print("✅ requirements.txt includes gunicorn")
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False
    
    # Test 3: Verify the app is a Flask instance
    try:
        from flask import Flask
        assert isinstance(app.app, Flask), "app should be a Flask instance"
        print("✅ app is a valid Flask instance")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    # Test 4: Check that app.run() is guarded (good for Render)
    with open('app.py', 'r') as f:
        app_content = f.read()
    
    if 'if __name__ == "__main__":' in app_content:
        print("✅ app.run() is properly guarded for local development")
    else:
        print("⚠️  app.run() might not be guarded (not critical for Render)")
    
    print("\n🎉 All Render compatibility checks passed!")
    return True

if __name__ == "__main__":
    test_render_compatibility()