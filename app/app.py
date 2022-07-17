from flask import Flask
from app.routes.routes import add_routes


app = Flask(__name__)

add_routes(app)
