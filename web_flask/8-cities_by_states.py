#!/usr/bin/python3

"""This script starts the flask application and runs the web server."""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def teardown_session(_):
    """Closes the current session after each request."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def get_cities_by_state():
    """
    Renders all the City objects by State objects available in the storage.
    """
    states = storage.all(State).values()

    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
