"""Web app for controlling lights through a Raspberry PI"""

import logging
from logging.handlers import RotatingFileHandler
import argparse
import os
from flask import Flask
from flask import request
from lights import Lights
from lights_pi import LightsPi
import json

from lights_sqlite_store import LightsSqliteStore

app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/toggle")
def toggle():
    lights.toggle("web")
    return json.dumps({"state": lights.get_state()})


@app.route("/api/state", methods=["GET", "PUT"])
def state():
    if request.method == "PUT":
        new_state = request.get_json()["state"] in ["true", 1, "True"]
        lights.set_state(new_state, "web")
    return json.dumps({"state": lights.get_state()})


@app.route("/api/triggers", methods=["GET", "PUT"])
def triggers():
    if request.method == "PUT":
        trigger = request.get_json()
        lights.add_trigger(**trigger)
    return json.dumps([t.__dict__ for t in lights.get_triggers()])


@app.route("/api/triggers/<job_id>", methods=["DELETE"])
def remove_trigger(job_id):
    lights.remove_trigger(job_id)
    return triggers()


@app.route("/api/stop")
def stop():
    lights.stop()
    return "{}"


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--pi", action='store_true', help="Run with Raspberry PI lights controller")
    parser.add_argument("--debug", action='store_true', help="Run with debug mode")
    return parser.parse_args()


def setup_logging():
    os.makedirs("log", exist_ok=True)
    handler = RotatingFileHandler("log/lights.log", backupCount=10)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Lights Starting...")

if __name__ == "__main__":
    args = parse_args()
    setup_logging()
    app.debug = args.debug
    os.makedirs("data", exist_ok=True)
    store = LightsSqliteStore("data/triggers.db")
    lights = LightsPi(store=store) if args.pi else Lights(store=store)
    lights.logger = app.logger
    app.run(host="0.0.0.0")
