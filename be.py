from flask import Flask
import flask
import sys

app = Flask(__name__)

@app.route("/")
def hello():
    print("Replied with a hello message")
    return f"Hello from Backend Server running on port {sys.argv[1]}", 200

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: python be.py PORT")
        exit()
    PORT = sys.argv[1]
    app.run(host="0.0.0.0", port=PORT, debug=True)
