from geopandas.geodataframe import GeoDataFrame
from osmnx.distance import euclidean_dist_vec


def get_close_nodes(
    df: GeoDataFrame, distance: float, x: float, y: float, nb_data=None
):
    my_df = df.copy(deep=True)
    my_df = my_df.to_crs("EPSG:3857")
    my_df["distance"] = euclidean_dist_vec(
        y, x, my_df["geometry"].y, my_df["geometry"].x
    )
    res = my_df[my_df["distance"] <= distance].sort_values(by="distance")

    if nb_data:
        res = res.head(nb_data)
    return res
