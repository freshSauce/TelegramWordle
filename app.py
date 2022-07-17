from flask import Flask
from config import DEBUG, PORT
from routes import add_routes


def build_app():
    app = Flask(__name__)
    add_routes(app)

if __name__ == "__main__":
    app = build_app()
    app.run(debug=DEBUG, port=PORT)
