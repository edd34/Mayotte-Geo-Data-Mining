from pprint import pprint
import geojson
import geopandas as gpd
import osmnx as ox
import overpass
from query import query
from helpers import get_close_nodes
from shapely.geometry import Polygon, Point

ox.config(use_cache=True, log_console=True)
api = overpass.API()

# step 1 : extract raw data from the dowloaded json
with open("./mayotte.json", mode="r") as f:
    data_load = geojson.load(f)["elements"]

# step 2 : transform data
gdf_raw = gpd.GeoDataFrame(data_load)
gdf_way = gdf_raw[gdf_raw["type"] == "way"]
gdf = gdf_raw[gdf_raw["type"] == "node"]
gdf.crs = {"init": "epsg:4326"}

# process gdf_way
print(gdf_way.head(), gdf_way.shape)
gdf_way = gdf_way[gdf_way["geometry"].str.len() >= 3]
print(gdf_way.head(), gdf_way.shape)
gdf_way["geometry"] = gdf_way["geometry"].apply(
    lambda x: Polygon([Point(i.get("lat"), i.get("lon")) for i in x]), 1
)
gdf_way["geometry"] = gdf_way["geometry"].centroid

# process gdf
gdf["geometry"] = gpd.points_from_xy(gdf["lon"], gdf["lat"])

# concat dataframes

# change projection to metric
gdf = gdf.to_crs("EPSG:3857")
print(gdf)


location = gdf.sample(1)
print("location", location)
print(float(location["geometry"].x), float(location["geometry"].y))
pprint(dict(location["tags"]))
POI = get_close_nodes(
    gdf, 500, float(location["geometry"].x), float(location["geometry"].y), 5
)

print(POI)

# step 3 : return data in a format easily readable and usable
