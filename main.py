import overpass
import geojson
import geopandas as gpd
from query import query
api = overpass.API()

with open("./test.json",mode="r") as f:
  data_load = geojson.load(f)["elements"]

# step 1 : extract raw data from the dowloaded json
# step 2 : transform data
# step 2.1 : get centroid of relation
# step 2.2 : get centroid 
# step 3 : return data in a format easily readable and usable

list_features = ["amenity", "shop"]
def my_custom_filter(features, x):
  check = all(item in features for item in list(x["tags"].keys()))
  if not check:
    return False
  if not x["type"] == "node":
    return False
  return True

res = filter(lambda x: my_custom_filter(list_features, x), data_load)
print(list(res))