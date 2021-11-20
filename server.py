from flask import Flask

from POI import POI

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<x>/<y>/<radius>/")
def show_user_profile(x, y, radius):
    poi = POI()
    res = poi.get_close_node(float(radius), float(x), float(y))
    return poi.clean_output_format(res)
