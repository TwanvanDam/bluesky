input_file = "trafficNE6.scn"
output_file = "trafficNE7.scn"


lines = []
targ_coord = '51.9618725 5.0541043'
targ_alt = 6000
targ_spd = 250

with open(input_file, "r") as file:
    for n,line in enumerate(file):
        if n < 2:
            lines.append(line)
            continue

 # Normalize the line
        if targ_coord in line:  # Check if the line contains "%0"
            line = line.strip('\n')
            new_line = line + ' 6000 250\n'
            lines.append(new_line)
            continue
        else:
            lines.append(line)

with open(output_file, "w") as file:
    file.writelines(lines)