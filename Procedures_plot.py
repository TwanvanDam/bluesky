import fiona
import math
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpl_toolkits.basemap import Basemap


def read_sector_file(file_path):
    fiona.supported_drivers['KML'] = 'rw'

    df = gpd.read_file(input_file, driver='KML', layer="Grenzen")
    sectors = df[df['geometry'].geom_type == 'Polygon'].reset_index()
    return sectors

def read_sid_star_file(file_path):
    """
    Read the SID/STAR file and return a GeoDataFrame.
    """
    fiona.supported_drivers['KML'] = 'rw'

    df = gpd.read_file(input_file, driver='KML', layer="SID/STAR")
    procedures = df[df['geometry'].geom_type == 'LineString']
    return procedures

def setup_map(resolution, plot_satellite, plot_configs, center_airport):
    plt.figure(figsize=plot_configs[center_airport]["figure_size"])
    m = Basemap(projection='merc',epsg=3857,
                llcrnrlat=plot_configs[center_airport]["map_size"]["min_lat"],
                urcrnrlat=plot_configs[center_airport]["map_size"]["max_lat"],
                llcrnrlon=plot_configs[center_airport]["map_size"]["min_lon"],
                urcrnrlon=plot_configs[center_airport]["map_size"]["max_lon"],
                resolution=resolution)

    m.drawcountries(linewidth=1)
    m.drawrivers()
    m.drawcoastlines()
    m.drawstates()

    if plot_satellite:
        m.arcgisimage(service='World_Imagery', xpixels=1500, verbose=False)
    else:
        m.drawmeridians(np.arange(math.floor(plot_configs[center_airport]["map_size"]["min_lon"]),
                                 math.ceil(plot_configs[center_airport]["map_size"]["max_lon"]), 1), labels=[0, 0,0,1], fontsize=10, linewidth=0.1, zorder=10)
        m.drawparallels(np.arange(math.floor(plot_configs[center_airport]["map_size"]["min_lat"]),
                                 math.ceil(plot_configs[center_airport]["map_size"]["max_lat"]), 1), labels=[1,0,0,0], fontsize=10, linewidth=0.1, zorder=10)
    return m

def plot_procedures(center_airport, procedures,map,  airport_coordinates_dict, plot_configs):
    colors = plot_configs[center_airport]["colors"]

    for i in range(len(procedures)):
        if center_airport in procedures["Name"][i][:3] or (center_airport == "Overview"):
            for key in colors.keys():
                if key in procedures["Name"][i]:
                    color = colors[key]
                    linestyle = "solid"
                    linewidth = 2
                    break

        else:
            color = "white"
            linestyle = "dashed"
            linewidth = 1
        x = procedures["geometry"][i].xy[0]
        y = procedures["geometry"][i].xy[1]
        if center_airport == "Overview":
            linewidth = 0.5

        plt.plot(*map(x, y), color=color, linestyle=linestyle, linewidth=linewidth)

        if center_airport != "Overview":
            for airport in airport_coordinates_dict.keys():
                if airport != "Overview":
                    x, y = airport_coordinates_dict[airport][:-1]
                    min_x = plot_configs[center_airport]["map_size"]["min_lon"]
                    max_x = plot_configs[center_airport]["map_size"]["max_lon"]
                    min_y = plot_configs[center_airport]["map_size"]["min_lat"]
                    max_y = plot_configs[center_airport]["map_size"]["max_lat"]
                    if min_x < x < max_x and min_y < y < max_y:
                        plt.plot(*map(*airport_coordinates_dict[airport][:-1]), 'ro', markersize=5)
                        plt.text(*map(x, y+0.02), airport_coordinates_dict[airport][2],
                                 fontsize=8, color="red", horizontalalignment="center")
    return

def plot_sector(sectors, map):
    for i in range(len(sectors)):
        if "Sector" in sectors["Name"][i]:
            x = sectors["geometry"][i].exterior.xy[0]
            y = sectors["geometry"][i].exterior.xy[1]
            centroid = sectors["geometry"][i].centroid.xy
            # print bold text
            if sectors["Name"][i] == "Sector 1":
                plt.text(*map(centroid[0][0], centroid[1][0]), "1", fontsize=10, color="white", horizontalalignment="center", weight="bold")
            else:
                plt.text(*map(centroid[0][0], centroid[1][0]), sectors["Name"][i], fontsize=10, color="white", horizontalalignment="center", weight="bold")
            plt.plot(*map(x, y), color="white", linestyle="solid", linewidth=2)

def make_legend(center_airport, sectors):
    for i in range(len(sectors)):
        handles = []
        for label, color in plot_configs[center_airport]["colors"].items():
            handle = mlines.Line2D([], [], color=color, label=label)
            handles.append(handle)
        if center_airport != "Overview":
            handles.append(mlines.Line2D([], [], color="white", linestyle="dashed", label=  "Routes to/from\n "
                                                                                                    "other airports"))
        handles.append(mlines.Line2D([], [], color="red", marker="o", linestyle="None", markersize=8, label="Airports"))

        plt.legend(handles=handles)


if __name__ == "__main__":
    course = False
    if course:
        resolution = "c"
        plot_satellite = False
    else:
        resolution = "h"
        plot_satellite = True

    input_file = "C:/Users/twanv/Downloads/ATM Kaart.kml"

    plot_configs = {"AMS" : {   "colors" :      {"SID 09": "yellow", "SID 36L": "orange", "STAR 04": "cyan", "STAR 06": "blue"},
                                "map_size" :    {"min_lat" : 51.7, "max_lat" : 52.8, "min_lon" : 2.5, "max_lon" : 7},
                                "figure_size" : (12, 5)},
                    # "RTM": {"colors":           {"SID 06": "yellow", "STAR 06": "cyan"},
                    #         "map_size":         {"min_lat": 51.5, "max_lat": 52.3, "min_lon": 3.2, "max_lon": 5.5},
                    #         "figure_size":      (9, 5)},
                    "LEY": {"colors": {"STAR": "cyan"},
                                 "map_size": {"min_lat": 51.8, "max_lat": 52.8, "min_lon": 4.8, "max_lon": 6.2},
                                 "figure_size": (5, 5)},
                    # "EIN": {"colors": {"SID": "yellow", "STAR": "cyan"},
                    #              "map_size": {"min_lat": 51.3, "max_lat": 51.7, "min_lon": 4.8, "max_lon": 6.3},
                    #              "figure_size": (12, 12)},
                    "MAA": {"colors": { "STAR": "cyan"},
                                 "map_size": {"min_lat": 50.7, "max_lat": 51, "min_lon": 5.5, "max_lon": 6},
                                 "figure_size": (5, 5)},
                    # "LWR": {"colors": { "STAR": "cyan"},
                    #              "map_size": {"min_lat": 53.15, "max_lat": 53.35, "min_lon": 5.5, "max_lon": 6},
                    #              "figure_size": (6, 6)},
                    # "GRQ": {"colors": {"STAR": "cyan"},
                    #              "map_size": {"min_lat": 52.4, "max_lat": 53.3, "min_lon": 5.4, "max_lon": 7},
                    #              "figure_size": (5, 5)},
                    #  "Overview" : {"colors":     {"SID": "yellow", "STAR": "cyan"},
                    #               "map_size":   {"min_lat": 50.5, "max_lat": 55, "min_lon": 2, "max_lon": 7.5},
                    #               "figure_size":(12, 12 )},
                         "UDE": {"colors": {"STAR": "cyan"},
                                  "map_size": {"min_lat": 51.6, "max_lat": 51.85, "min_lon": 5.3, "max_lon": 5.8},
                                  "figure_size": (5, 5)},
                     "ENS": {"colors": {"STAR": "cyan"},
                             "map_size": {"min_lat": 52.2, "max_lat": 52.35, "min_lon": 6.7, "max_lon": 7},
                             "figure_size": (5, 5)},
                     "DHR": {"colors": {"STAR": "cyan"},
                             "map_size": {"min_lat": 52.8, "max_lat": 53, "min_lon": 4.5, "max_lon": 5.1},
                             "figure_size": (6, 6)}}

    airport_coordinates_dict = {
        "RTM": [4.4595, 51.9644, "EHRD"], # Rotterdam airport
        "AMS": [4.7681, 52.3105, "EHAM"], # Amsterdam airport
        "LEY": [5.5189, 52.4557, "EHLE"], # Lelystad airport
        "EIN": [5.3761, 51.4516, "EHEH"], # Eindhoven airport
        "UDE": [5.7091, 51.6577, "EHVK"], # Volkel airport
        "MAA": [5.7712, 50.9130, "EHBK"], # Maastricht airport
        "LWR": [5.7601, 53.2285, "EHLW"], # Leeuwarden airport
        "GRQ": [6.5773, 53.1189, "EHGG"], # Groningen airport
        "ENS": [6.8859, 52.2745, "EHTW"], # Twente airport
        "DHR": [4.7807, 52.9236, "EHDK"], # De kooy airport
    }

    procedures = read_sid_star_file(input_file)
    sectors = read_sector_file(input_file)

    for airport in plot_configs.keys():
        m = setup_map(resolution, plot_satellite, plot_configs, airport)

        plot_procedures(airport, procedures, m, airport_coordinates_dict, plot_configs)
        if airport == "Overview":
            plot_sector(sectors, m)
        make_legend(airport, sectors)
        plt.savefig(f"./procedures/plots/{airport}.png", bbox_inches='tight', dpi=200)
        plt.show()