import osmnx as ox

ox.config(use_cache=True, log_console=True)
# G = ox.graph_from_place("Mayotte", simplify=False)
gdf_osmnx = ox.geometries_from_place("Mayotte", tags={"building": True})

print(gdf_osmnx)
