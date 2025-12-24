from app import create_app

# Create the application using the factory
app = create_app()

if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True, port=5001)

