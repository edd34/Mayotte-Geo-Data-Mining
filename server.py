from flask import Flask

from POI import POI

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<x_lon>/<y_lat>/<radius>/")
def show_user_profile(x_lon, y_lat, radius):
    poi = POI()
    res = poi.get_close_node(float(radius), float(x_lon), float(y_lat))
    # print(res)
    # print(poi.clean_output_format(res))
    return poi.clean_output_format(res)


app.run(debug=True)
