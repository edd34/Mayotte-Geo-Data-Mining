import geojson
import geopandas as gpd
from osmnx.distance import euclidean_dist_vec
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon

P3857 = Proj(init="epsg:3857")
P4326 = Proj(init="epsg:4326")


class POI:
    def __init__(self):
        with open("./mayotte.json", mode="r") as f:
            self._data_load = geojson.load(f)["elements"]
        self._gdf = gpd.GeoDataFrame(self._data_load, crs="EPSG:4326")
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

    def get_close_node(self, distance: float, x_lon: float, y_lat: float, nb_data=None):
        gdf = self._gdf.to_crs("EPSG:3857")
        x, y = transform(P4326, P3857, x_lon, y_lat)
        gdf["distance"] = euclidean_dist_vec(y, x, gdf["geometry"].y, gdf["geometry"].x)
        res = gdf[gdf["distance"] <= distance].sort_values(by="distance")

        if nb_data:
            res = res.head(nb_data)

        res = res.to_crs("EPSG:4326")
        return res

    def clean_output_format(self, POI):
        list_markers = list(POI["geometry"])
        # step 3 : return data in a format easily readable and usable

        POI = POI.to_crs("EPSG:4326")
        list_markers = list(POI["geometry"])
        clean_list_markers = [
            (list_markers[i].x, list_markers[i].y) for i in range(1, len(list_markers))
        ]
        return clean_list_markers
