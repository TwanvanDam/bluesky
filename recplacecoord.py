input_file = "trafficNE6.scn"
output_file = "trafficNE7.scn"


lines = []
targ_coord = '52.2380841 4.8958662'
new_coord = '52.2781906 4.9646874'

with open(input_file, "r") as file:
    for n,line in enumerate(file):
        if n < 2:
            lines.append(line)
            continue

 # Normalize the line
        if targ_coord in line:  # Check if the line contains "%0"
            modified_line = line.replace(targ_coord, new_coord)
            lines.append(modified_line)
        else:
            lines.append(line)

with open(output_file, "w") as file:
    file.writelines(lines)