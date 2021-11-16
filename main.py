from geopandas.geodataframe import GeoDataFrame
import osmnx as ox
from osmnx.distance import euclidean_dist_vec
from pprint import pprint
import overpass
import geojson
import geopandas as gpd
from query import query
from pyproj import Proj

ox.config(use_cache=True, log_console=True)
# G = ox.graph_from_place("Mayotte", simplify=False)
# gdf_osmnx = ox.geometries_from_place("Mayotte")

api = overpass.API()

# step 1 : extract raw data from the dowloaded json
with open("./mayotte.json", mode="r") as f:
    data_load = geojson.load(f)["elements"]

# step 2 : transform data
list_features = ["amenity", "shop"]


def my_custom_filter(features, x):
    # check = all(item in features for item in list(x["tags"].keys()))
    # if not check and not x["type"] == "node":
    if not x["type"] == "node":
        return False
    return True


data_load = filter(lambda x: my_custom_filter(list_features, x), data_load)
# pprint(list(res))

gdf = gpd.GeoDataFrame(data_load)
gdf.crs = {"init": "epsg:4326"}


gdf["geometry"] = gpd.points_from_xy(gdf["lon"], gdf["lat"])
print(gdf)
gdf = gdf.to_crs("EPSG:3857")
print(gdf)


def get_close_nodes(df: GeoDataFrame, distance: float, x: float, y: float):
    my_df = df.copy(deep=True)
    my_df["distance"] = euclidean_dist_vec(
        y, x, my_df["geometry"].y, my_df["geometry"].x
    )
    return my_df[my_df["distance"] <= distance].sort_values(by="distance")


location = gdf.sample(1)
print(location)
print(float(location["geometry"].x), float(location["geometry"].y))
pprint(dict(location["tags"]))
POI = get_close_nodes(
    gdf, 50000000000, float(location["geometry"].x), float(location["geometry"].y)
)

print(POI)

# step 3 : return data in a format easily readable and usable
