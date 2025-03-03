import fiona
import os
import shutil
import geopandas as gpd

if os.path.exists("./procedures"):
    shutil.rmtree("./procedures")
os.mkdir("./procedures")

# Enable KML support via fiona
fiona.supported_drivers['KML'] = 'rw'

df = gpd.read_file('ATM Kaart.kml', driver='KML', layer="SID/STAR")
procedures = df[df['geometry'].geom_type == 'LineString'].reset_index()
for i in range(len(procedures)):
    lines = []
    if "RTM" in procedures["Name"][i]:
        origin = [4.4595321, 51.9644045]
    elif "AMS" in procedures["Name"][i]:
        origin = [4.7681, 52.3105]
    else:
        raise ValueError("Unknown airport")
    points = procedures["geometry"][i].coords

    if "SID" in procedures["Name"][i]:
        distance_first = (points[0][0] - origin[0]) ** 2 + (points[0][1] - origin[1]) ** 2
        distance_last = (points[-1][0] - origin[0]) ** 2 + (points[-1][1] - origin[1]) ** 2
        if distance_first > distance_last:
            points = list(reversed(points))
            print(f"{procedures["Name"][i]} line reversed")
        points =  points[1:] # Remove first point (departure airport)

    if "STAR" in procedures["Name"][i]:
        distance_first = (points[0][0] - origin[0]) ** 2 + (points[0][1] - origin[1]) ** 2
        distance_last = (points[-1][0] - origin[0]) ** 2 + (points[-1][1] - origin[1]) ** 2
        if distance_first < distance_last:
            points = list(reversed(points))
            print(f"{procedures["Name"][i]} line reversed")
        points =  points[:-1] # Remove last point (arrival airport)


    for point in points:
        lines.append(f"00:00:00.00>%0 addwpt {point[1]} {point[0]}\n")

    file_name = (f"./procedures/{procedures["Name"][i]}.scn"
                 .replace(" ", "_").replace("South", "S").replace("North", "N")
                 .replace("East", "E").replace("West", "W").replace("-", ""))

    with open(file_name, "w") as text_file:
        text_file.writelines(lines)



