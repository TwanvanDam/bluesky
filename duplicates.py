input_file = "trafficNE4.scn"
output_file = "trafficNE5.scn"

def string_to_time(str):
    """Convert a string to a time object."""
    hour = line[0:2]
    minutes = line[3:5]
    seconds = line[6:8]
    hundredths = line[9:11]
    time = (3600 * int(hour) + 60 * int(minutes) + int(seconds)) * 100 + int(hundredths)
    return time

def time_to_string(time):
    """Convert a time object to a string."""
    hour = str(time // 360000)
    minutes = str((time % 360000) // 6000)
    seconds = str((time % 6000) // 100)
    hundredths = str(time % 100)
    return f"{hour.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}.{hundredths.zfill(2)}"

seen = set()
unique_lines = []

with open(input_file, "r") as file:
    for n,line in enumerate(file):
        if n < 2:  # Skip the first two lines
            seen.add(line)
            unique_lines.append(line)
            continue
        line = line.upper().replace(",", " ")  # Normalize the line
        if "%0" in line:  # Check if the line contains "%0"
            print(f"Line {n}: {line} contains %0")
            continue

        time = string_to_time(line)
        line_increment = time_to_string(time-1) + line[11:]  # Decrement the number in the line
        if (line not in seen) and (line_increment not in seen):  # Check if line is unique
            seen.add(line)
            unique_lines.append(line)
        else:
            print(f"Duplicate line found: {line} already in set as {line_increment}")

# Write unique lines back to file, keeping the original order
with open(output_file, "w") as file:
    file.writelines(unique_lines)
