from POI import POI

if __name__ == "__main__":
    poi = POI()
    res = poi.get_close_node(500, -12.843990, 45.187113)
    print(poi.clean_output_format(res))
