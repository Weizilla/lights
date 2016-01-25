import flask
from flask import Flask

app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/hello")
def hello():
    d = {"hello": "world"}
    return flask.jsonify(d)


if __name__ == "__main__":
    app.debug = True
    app.run()
