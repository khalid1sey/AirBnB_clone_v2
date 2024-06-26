#!/usr/bin/python3

"""This module contains routes for the AirBnB web project."""

from markupsafe import escape
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """Returns a simple string for the homepage."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Handles the /hbnb route."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Returns a note about the C language."""
    return f"C {escape(text.replace('_', ' '))}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
