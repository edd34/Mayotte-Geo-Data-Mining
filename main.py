from pprint import pprint

import geojson
import geopandas as gpd
import osmnx as ox
import overpass
from geopandas.geodataframe import GeoDataFrame
from osmnx.distance import euclidean_dist_vec
from pyproj import Proj

from query import query

ox.config(use_cache=True, log_console=True)
api = overpass.API()

# step 1 : extract raw data from the dowloaded json
with open("./mayotte.json", mode="r") as f:
    data_load = geojson.load(f)["elements"]

# step 2 : transform data
gdf = gpd.GeoDataFrame(data_load)
gdf = gdf[gdf["type"] == "node"]
gdf.crs = {"init": "epsg:4326"}


gdf["geometry"] = gpd.points_from_xy(gdf["lon"], gdf["lat"])
gdf = gdf.to_crs("EPSG:3857")
print(gdf)


def get_close_nodes(
    df: GeoDataFrame, distance: float, x: float, y: float, nb_data=None
):
    my_df = df.copy(deep=True)
    my_df["distance"] = euclidean_dist_vec(
        y, x, my_df["geometry"].y, my_df["geometry"].x
    )
    res = my_df[my_df["distance"] <= distance].sort_values(by="distance")

    if nb_data:
        res = res.head(nb_data)
    return res


location = gdf.sample(1)
print(location)
print(float(location["geometry"].x), float(location["geometry"].y))
pprint(dict(location["tags"]))
POI = get_close_nodes(
    gdf, 500, float(location["geometry"].x), float(location["geometry"].y), 20
)

print(POI)

# step 3 : return data in a format easily readable and usable
