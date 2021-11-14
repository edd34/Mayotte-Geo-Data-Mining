import overpass
import geojson
import geopandas as gpd
from query import query
api = overpass.API()

res = api.get(query, build=False)

with open("./test.json",mode="w") as f:
  geojson.dump(res,f)
