import geojson
import geopandas as gpd
from shapely.geometry import Point, Polygon

from helpers import get_close_nodes
from query import query
from osmnx.distance import euclidean_dist_vec


class POI:
    def __init__(self):
        with open("./mayotte.json", mode="r") as f:
            self._data_load = geojson.load(f)["elements"]
        self._gdf = gpd.GeoDataFrame(self.data_load, crs="EPSG:4326")
        self._pre_process_data()
        self._process_data()

    def _pre_process_data(self):
        self._gdf = self._gdf[self._gdf["geometry"].str.len() >= 3]

    def _process_data(self):
        gdf_node = self._gdf[self._gdf["type"] == "node"]
        gdf_way = self._gdf[self._gdf["type"] == "way"]

        # process gdf node
        gdf_node["geometry"] = gpd.points_from_xy(gdf_node["lat"], gdf_node["lon"])

        # process gdf way
        gdf_way["geometry"] = gdf_way["geometry"].apply(
            lambda x: Polygon([Point(i.get("lat"), i.get("lon")) for i in x]), 1
        )
        gdf_way["geometry"] = gdf_way["geometry"].centroid

        self._gdf = gdf_node.append(gdf_way, ignore_index=True)

    def get_close_node(self, distance: float, x: float, y: float, nb_data=None):
        gdf = self._gdf.to_crs("EPSG:3857")
        gdf["distance"] = euclidean_dist_vec(y, x, gdf["geometry"].y, gdf["geometry"].x)
        res = gdf[gdf["distance"] <= distance].sort_values(by="distance")

        if nb_data:
            res = res.head(nb_data)

        gdf = gdf.to_crs("EPSG:4326")
        return gdf

    def clean_output_format(self):
        pass
