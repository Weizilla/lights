import flask
from flask import Flask
from flask import request
from lights import Lights

app = Flask(__name__, static_url_path="")
lights = Lights()


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/toggle")
def toggle():
    lights.toggle_light()


@app.route("/api/lights/<light>")
def set_lights(light):
    lights.set_light(light)
    return light

@app.route("/api/lights")
def get_lights():
    return str(lights.get_light())


@app.route("/api/time/<mode>", methods=["GET", "PUT"])
def set_time(mode):
    print("method: {} form {}".format(request.method, request.form))
    if request.method == "PUT":
        lights.set_time(mode, request.form["time"])
    mode = lights.get_time(mode)
    return mode or ""


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
