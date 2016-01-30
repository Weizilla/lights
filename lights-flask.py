"""Web app for controlling lights through a Raspberry PI"""

import flask
import argparse
from flask import Flask
from flask import request
from lights import Lights
from lights_pi import LightsPi

app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/toggle")
def toggle():
    lights.toggle_light()


@app.route("/api/lights/<light>")
def set_lights(light):
    lights.set_light(light)
    return flask.jsonify({"light": light})


@app.route("/api/lights")
def get_lights():
    return flask.jsonify({"light": lights.get_light()})


@app.route("/api/times")
def get_times():
    return flask.jsonify(lights.get_times())


@app.route("/api/times/<mode>", methods=["GET", "PUT"])
def set_time(mode):
    print("method: {} form {}".format(request.method, request.form))
    if request.method == "PUT":
        lights.set_time(mode, request.form["time"])
    time = lights.get_time(mode)
    return flask.jsonify({mode: time}) or "{}"


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
