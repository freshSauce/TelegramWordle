from app import app
from config import DEBUG, PORT


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
