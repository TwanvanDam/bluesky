import pandas as pd

with open("../trafficNE.scn", "r") as f:
    lines = f.readlines()

flights = []
for i in range(len(lines)):
    line = lines[i]
    if "CRE" in line:
        time = line.split(" ")[0].split(">")[0]
        call_sign = line.split(" ")[1]
        aircraft_type = line.split(" ")[2]

        origin = ""
        destination = ""
        heading = None
        for j in range(5):
            if call_sign not in lines[i + j]:
                continue
            if "ORIG" in lines[i+j]:
                origin = lines[i + j].split(" ")[-1][:-1]
                if len(origin) > 4:
                    origin = "Coordinate"
            if "HDG" in lines[i+j+1]:
                print(lines[i + j+1])
                heading =  f"{round(float(lines[i + j + 1].split(" ")[2][:-1]) / 10):02d}"
                if heading == "00":
                    heading = "36"

            if "DEST" in lines[i+j]:
                destination = lines[i + j].split(" ")[-1][:-1]
                if len(destination) > 4:
                    destination = "Coordinate"
        flights.append({"time": time, "call_sign": call_sign, "aircraft_type": aircraft_type, "origin_icao": origin,"runway":heading, "destination_icao": destination})
df = pd.DataFrame(flights)

def load_airport_mapping(csv_path):
    """Load ICAO to airport name mapping from a large CSV file using chunking."""
    airport_mapping = {}
    chunksize = 10**6  # Adjust the chunksize as needed
    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        # Assuming the CSV has columns 'icao' and 'name'
        subset = chunk[['ident', 'name']].dropna()
        mapping = dict(zip(subset['ident'], subset['name']))
        airport_mapping.update(mapping)
    return airport_mapping

# Load the mapping dictionary from the airport CSV file.
airport_csv = './flat-ui__data-Mon Feb 24 2025.csv'  # adjust the path as required
icao_to_name = load_airport_mapping(airport_csv)

# Suppose you have a DataFrame `df` with 'origin' and 'destination' columns storing ICAO codes.
# Add the corresponding airport names to the DataFrame.
df['origin'] = df['origin_icao'].map(icao_to_name)
df['destination'] = df['destination_icao'].map(icao_to_name)
# Replace all NaN values with "Coordinate"
df['origin'].fillna("Coordinate", inplace=True)
df['destination'].fillna("Coordinate", inplace=True)

print(df)
df.to_excel("./flights.xlsx")