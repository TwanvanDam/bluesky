import fiona
import os
import shutil
import geopandas as gpd

def cleanup_saving_path(path):
    """
    Cleanup the saving path if it exists.
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    return

def read_sid_star_file(file_path):
    """
    Read the SID/STAR file and return a GeoDataFrame.
    """
    fiona.supported_drivers['KML'] = 'rw'

    df = gpd.read_file(input_file, driver='KML', layer="SID/STAR")
    procedures = df[df['geometry'].geom_type == 'LineString']
    sid = procedures[procedures["Name"].str.contains("SID")].reset_index()
    star = procedures[procedures["Name"].str.contains("STAR")].reset_index()
    return sid, star

def read_sector_file(file_path):
    fiona.supported_drivers['KML'] = 'rw'

    df = gpd.read_file(input_file, driver='KML', layer="Grenzen")
    sectors = df[df['geometry'].geom_type == 'Polygon'].reset_index()
    return sectors

def write_file(procedure_name, lines, save_path="./procedures"):
    """
    Write the lines to a file.
    """
    file_name = (f"{save_path}/{procedure_name}.scn"
                 .replace(" ", "_").replace("South", "S").replace("North", "N")
                 .replace("East", "E").replace("West", "W").replace("-", ""))
    with open(file_name, "w") as text_file:
        text_file.writelines(lines)

def save_sids_to_file(sids, airport_coordinates_dict, save_path="./procedures"):
    for i in range(len(sids)):
        lines = []

        # get departure airport coordinates
        departure_aiport_coordinate = airport_coordinates_dict.get(str(sids["Name"][i])[:3].upper())
        if not departure_aiport_coordinate:
            print(f"Unknown airport {str(sids["Name"][i])[:3].upper()}, skipping...")
            continue
        points = sids["geometry"][i].coords

        # check if the line is reversed
        distance_first = (points[0][0] - departure_aiport_coordinate[0]) ** 2 + (points[0][1] - departure_aiport_coordinate[1]) ** 2
        distance_last = (points[-1][0] - departure_aiport_coordinate[0]) ** 2 + (points[-1][1] - departure_aiport_coordinate[1]) ** 2
        if distance_first > distance_last:
            points = list(reversed(points))
            print(f"{sids['Name'][i]} line reversed")

        points = points[1:]  # Remove first point (departure airport is already in the flight plan)
        color = "yellow"

        # save all points as waypoints
        for point in points:
            lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]}\n")

        # add altitude, speed and color
        lines.append(f"00:00:00.10>%0 COL {color}\n")
        lines.append(f"00:00:00.10>%0 ALT FL300\n")
        lines.append(f"00:00:00.10>%0 ATALT FL100 SPD 350\n")

        # save the file
        write_file(sids['Name'][i], lines, save_path)
    return

def save_stars_to_file(stars, airport_coodinates_dict, save_path="./procedures"):
    for i in range(len(stars)):
        lines = []

        # get arrival airport coordinates
        arrival_airport_coordinate = airport_coodinates_dict.get(str(stars["Name"][i])[:3].upper())
        if not arrival_airport_coordinate:
            print(f"Unknown airport {str(stars["Name"][i])[:3].upper()}, skipping...")
            continue

        points = stars["geometry"][i].coords

        # check if the line is reversed
        distance_first = (points[0][0] - arrival_airport_coordinate[0]) ** 2 + (points[0][1] - arrival_airport_coordinate[1]) ** 2
        distance_last = (points[-1][0] - arrival_airport_coordinate[0]) ** 2 + (points[-1][1] - arrival_airport_coordinate[1]) ** 2
        if distance_first < distance_last:
            points = list(reversed(points))

        # save all points as waypoints
        for j, point in enumerate(points):
            # if j == 0:
            #     lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} 9000 250\n")

            # second to last point (=start of runway) set speed to 150
            if j == len(points) - 2:
                lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} 0 150\n")

            # last point (=end of runway) set speed to 0
            elif j == len(points) - 1:
                lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} 0 0\n")
            else:
                lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]}\n")

        # add altitude, speed and color
        lines.append(f"00:00:00.10>%0 COL blue\n")
        lines.append(f"00:00:00.10>%0 ATALT FL100 SPD 250\n")
        lines.append(f"00:00:00.15>%0 VNAV on\n")

        # save the file
        write_file(stars['Name'][i], lines, save_path)

def save_sectors_to_file(sectors, save_path="./procedures"):
    lines = []
    for i in range(len(sectors)):
        if "Sector" in sectors["Name"][i]:
            # make .scn file to plot the sector in bluesky
            line = f"00:00:00.10>POLY {sectors["Name"][i].replace(" ", "_")} "
            points = sectors["geometry"][i].exterior.coords
            for point in points:
                line += f"{point[1]} {point[0]} "

            lines += [line + "\n"]

    file_name = "sectors"
    write_file(file_name, lines, save_path)
    return

if __name__ == "__main__":
    input_file = "C:/Users/twanv/Downloads/ATM Kaart.kml"
    cleanup_saving_path("./procedures")

    airport_coordinates_dict = {
        "RTM": [4.4595, 51.9644], # Rotterdam airport
        "AMS": [4.7681, 52.3105], # Amsterdam airport
        "LEL": [5.5189, 52.4557], # Lelystad airport
        "EIN": [5.3761, 51.4516], # Eindhoven airport
        "UDE": [5.7091, 51.6577], # Volkel airport
        "MAA": [5.7712, 50.9130], # Maastricht airport
        "LEE": [5.7601, 53.2285], # Leeuwarden airport
        "GRO": [6.5773, 53.1189], # Groningen airport
        "TWE": [6.8859, 52.2745], # Twente airport
        "HOO": [6.5183, 52.7309], # Hoogeveen airport
        "ZEE": [3.7307, 51.5122], # Midden zeeland airport
        "KOO": [4.7807, 52.9236], # De kooy airport
        "TEU": [6.0499, 52.2428], # Teuge airport
    }

    # Save sectors to file
    sectors = read_sector_file(input_file)
    save_sectors_to_file(sectors)

    # Save SIDs and STARs to files
    sids, stars = read_sid_star_file(input_file)
    save_sids_to_file(sids, airport_coordinates_dict)
    save_stars_to_file(stars, airport_coordinates_dict)



