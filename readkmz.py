import fiona
import os
import shutil
import geopandas as gpd

input_file = "C:/Users/twanv/Downloads/ATM Kaart.kml"


if os.path.exists("./procedures"):
    shutil.rmtree("./procedures")
os.mkdir("./procedures")

# Enable KML support via fiona
fiona.supported_drivers['KML'] = 'rw'

df = gpd.read_file(input_file, driver='KML', layer="SID/STAR")
procedures = df[df['geometry'].geom_type == 'LineString'].reset_index()
waypoints = df[df['geometry'].geom_type == 'Point'].reset_index()

for i in range(len(waypoints)):
    with open(f"./procedures/{waypoints["Name"][i]}.scn", "w") as text_file:
        text_file.write(f"00:00:00.00>%0 addwpt {waypoints["geometry"][i].coords[0][1]} {waypoints["geometry"][i].coords[0][0]} 0 150\n")
        text_file.write(f"00:00:00.10>%0 COL yellow\n")

for i in range(len(procedures)):
    print(f"Processing {procedures["Name"][i]}")
    lines = []
    if "RTM" in procedures["Name"][i]:
        origin = [4.4595321, 51.9644045]
    elif "AMS" in procedures["Name"][i]:
        origin = [4.7681, 52.3105]
    elif "LEL" in procedures["Name"][i] or "LeGro" in procedures["Name"][i]:
        origin = [5.5189, 52.4557]
    elif "EIN" in procedures["Name"][i]:
        origin = [5.3761, 51.4516]
    else:
        raise ValueError(f"Unknown airport {procedures['Name'][i]}")
    points = procedures["geometry"][i].coords

    if "SID" in procedures["Name"][i]:
        distance_first = (points[0][0] - origin[0]) ** 2 + (points[0][1] - origin[1]) ** 2
        distance_last = (points[-1][0] - origin[0]) ** 2 + (points[-1][1] - origin[1]) ** 2
        if distance_first > distance_last:
            points = list(reversed(points))
            print(f"{procedures["Name"][i]} line reversed")
        points =  points[1:] # Remove first point (departure airport)
        color = "yellow"

    if "STAR" in procedures["Name"][i]:
        distance_first = (points[0][0] - origin[0]) ** 2 + (points[0][1] - origin[1]) ** 2
        distance_last = (points[-1][0] - origin[0]) ** 2 + (points[-1][1] - origin[1]) ** 2
        if distance_first < distance_last:
            points = list(reversed(points))
            print(f"{procedures["Name"][i]} line reversed")
        # points =  points[:-1] # Remove last point (arrival airport)
        color = "blue"

    # for point in points:
    #     lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} \n")
    for j, point in enumerate(points):
        if j == len(points) - 1:
            if ("STAR" in procedures["Name"][i]) or ("LeGro" in procedures["Name"][i]):
                lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} 0 150\n")
            else:
                lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} \n")
        if (j == 0) and ("STAR" in procedures["Name"][i]):
            lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]} 9000 250\n")

        else:
            lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]}\n")

    if "STAR" in procedures["Name"][i]:
        lines.append(f"00:00:00.10>%0 COL {color}\n")
        lines.append(f"00:00:00.10>%0 ATALT FL100 SPD 250\n")
        lines.append(f"00:00:00.15>%0 VNAV on\n")
    if "SID" in procedures["Name"][i]:
        lines.append(f"00:00:00.10>%0 COL {color}\n")
        lines.append(f"00:00:00.10>%0 ALT FL300\n")
        lines.append(f"00:00:00.10>%0 ATALT FL100 SPD 350\n")

    file_name = (f"./procedures/{procedures["Name"][i]}.scn"
                 .replace(" ", "_").replace("South", "S").replace("North", "N")
                 .replace("East", "E").replace("West", "W").replace("-", ""))
    print(f"Writing {file_name}")
    with open(file_name, "w") as text_file:
        text_file.writelines(lines)

df = gpd.read_file(input_file, driver='KML', layer="Grenzen")
df_sectors = df[df['geometry'].geom_type == 'Polygon'].reset_index()
lines = []
for i in range(len(df_sectors)):
    if "Sector" in df_sectors["Name"][i]:
        # make .scn file to plot the sector in bluesky
        line = f"00:00:00.10>POLY {df_sectors["Name"][i].replace(" ", "_")} "
        points = df_sectors["geometry"][i].exterior.coords
        for point in points:
            line += f"{point[1]} {point[0]} "

        lines += [line + "\n"]
file_name = f"./procedures/sectors.scn"
with open(file_name, "w") as text_file:
    text_file.writelines(lines)



