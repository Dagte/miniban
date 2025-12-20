from flask import Flask

print("The value of __name__ is:", __name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True)

