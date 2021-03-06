from pprint import pprint

import geojson
import geopandas as gpd
from shapely.geometry import Point, Polygon

from helpers import get_close_nodes
from query import query

# step 1 : extract raw data from the dowloaded json
with open("./mayotte.json", mode="r") as f:
    data_load = geojson.load(f)["elements"]

# step 2 : transform data
gdf_raw = gpd.GeoDataFrame(data_load)
gdf_way = gdf_raw[gdf_raw["type"] == "way"]
gdf = gdf_raw[gdf_raw["type"] == "node"]
gdf.crs = {"init": "epsg:4326"}

# process gdf_way
gdf_way = gdf_way[gdf_way["geometry"].str.len() >= 3]
gdf_way["geometry"] = gdf_way["geometry"].apply(
    lambda x: Polygon([Point(i.get("lat"), i.get("lon")) for i in x]), 1
)
gdf_way["geometry"] = gdf_way["geometry"].centroid

# process gdf
gdf["geometry"] = gpd.points_from_xy(gdf["lat"], gdf["lon"])

# concat dataframes
gdf = gdf.append(gdf_way, ignore_index=True)
# change projection to metric
# gdf = gdf.to_crs("EPSG:3857")

location = gdf.to_crs("EPSG:3857").sample(1)
# todo : use log
# print("location", location)
# print(float(location["geometry"].x), float(location["geometry"].y))
# pprint(dict(location["tags"]))
POI = get_close_nodes(
    gdf, 400, float(location["geometry"].x), float(location["geometry"].y), 20
)

# TODO : use log
# print(POI, POI[POI["type"] == "node"].shape, POI[POI["type"] == "way"].shape)
list_markers = list(POI["geometry"])
# step 3 : return data in a format easily readable and usable

POI = POI.to_crs("EPSG:4326")
list_markers = list(POI["geometry"])
print(list_markers)
clean_list_markers = [
    (list_markers[i].x, list_markers[i].y) for i in range(1, len(list_markers))
]
pprint(location)
pprint(clean_list_markers)
