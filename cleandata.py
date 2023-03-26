input_file = "data.csv"
output_file = "cleaneddata.csv"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    lines = infile.readlines()
    previous_value = None
    current_timestamp = None
    current_value = None

    for ligne in lines:
        if "Error: Data not found" in ligne:
            if previous_value:
                outfile.write(f"{current_timestamp}, {previous_value}\n")
        else:
            parts = ligne.strip().split(", ")

            if len(parts) == 2:
                current_timestamp, current_value = parts
            elif len(parts) == 1:
                current_value = parts[0]
                outfile.write(f"{current_timestamp}, {current_value}\n")
                previous_value = current_value
