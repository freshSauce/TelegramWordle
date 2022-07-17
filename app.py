from flask import Flask
from serialize import receive_info


app = Flask(__name__)


app.add_url_rule("/receive_info", view_func=receive_info, methods=["POST", "GET"])
