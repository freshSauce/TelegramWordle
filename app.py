from flask import Flask
from config import DEBUG, PORT
from serialize import receive_info


app = Flask(__name__)


@app.route("/")
def index():
    return "Test"


app.add_url_rule("/receive_info", view_func=receive_info, methods=["POST", "GET"])

if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
