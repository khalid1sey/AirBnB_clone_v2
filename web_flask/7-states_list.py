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


@app.route("/states_list", strict_slashes=False)
def get_states():
    """Renders all the State objects available in the storage."""
    states = storage.all(State).values()

    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
