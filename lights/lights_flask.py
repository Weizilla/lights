"""Web app for controlling lights through a Raspberry PI"""

import time
import flask
import argparse
from flask import Flask
from flask import request
from lights.lights import Lights
from lights.lights_pi import LightsPi
import json

app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/toggle")
def toggle():
    lights.toggle()
    return json.dumps({"state": lights.state})


@app.route("/api/state", methods=["GET", "PUT"])
def state():
    if request.method == "PUT":
        lights.state = request.get_json()["state"] in ["true", 1, "True"]
    return json.dumps({"state": lights.state})


@app.route("/api/triggers", methods=["GET", "PUT"])
def set_time():
    if request.method == "PUT":
        times = request.get_json()
        for (k, v) in times.items():
            lights.set_time(k, v)
    return flask.jsonify(lights.get_times())


@app.route("/api/stop")
def stop():
    lights.stop()
    return "{}"


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--pi", action='store_true', help="Run with Raspberry PI lights controller")
    parser.add_argument("--debug", action='store_true', help="Run with debug mode")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if (args.debug):
        app.debug = True
    if (args.pi):
        lights = LightsPi()
    else:
        lights = Lights()
    app.run(host="0.0.0.0")
