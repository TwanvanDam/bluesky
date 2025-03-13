input_file = "trafficNE3.scn"
output_file = "trafficNE4.scn"



seen = set()
unique_lines = []

with open(input_file, "r") as file:
    for line in file:
        if line not in seen:  # Check if line is unique
            seen.add(line)
            unique_lines.append(line)

# Write unique lines back to file, keeping the original order
with open(output_file, "w") as file:
    file.writelines(unique_lines)
