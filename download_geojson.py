import overpass
import geojson
from query import query

api = overpass.API()

res = api.get(query, build=False)

with open("./mayotte.json", mode="w") as f:
    geojson.dump(res, f)
