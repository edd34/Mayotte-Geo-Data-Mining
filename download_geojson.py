import geojson
import overpass

from query import query

api = overpass.API()

res = api.get(query, build=False)

with open("./mayotte.json", mode="w") as f:
    geojson.dump(res, f)
