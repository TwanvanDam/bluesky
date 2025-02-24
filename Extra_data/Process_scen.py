import pandas as pd

with open("./trafficNE.scn", "r") as f:
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
        for j in range(5):
            if call_sign not in lines[i + j]:
                continue
            if "ORIG" in lines[i+j]:
                origin = lines[i + j].split(" ")[-1][:-1]
                if len(origin) > 4:
                    origin = "Coordinate"
            if "DEST" in lines[i+j]:
                destination = lines[i + j].split(" ")[-1][:-1]
                if len(destination) > 4:
                    destination = "Coordinate"
        flights.append({"time": time, "call_sign": call_sign, "aircraft_type": aircraft_type, "origin": origin, "destination": destination})



df = pd.DataFrame(flights)
print(df.sort_values(by=["aircraft_type"]))
df.to_excel("./flights.xlsx")