import re

# Initialize a dictionary to store the z-component of torque for each part
torque_z = {}

# Open the file for reading
with open('polyflow.lst', 'r') as file:
    # Read the entire file content
    content = file.read()

    # Define a regular expression pattern to match the torque line
    pattern = r'torque\s*=\s*\(\s*(-?\d+\.\d+E[+-]?\d+)\s*,\s*(-?\d+\.\d+E[+-]?\d+)\s*,\s*(-?\d+\.\d+E[+-]?\d+)\)'

    # Find all matches in the file content
    matches = re.findall(pattern, content)

    # Iterate over the matches
    for match in matches:
        # Extract the part number from the line before the match
        part_number = re.search(r'moving part #(\d+)', content[:content.find(match[0])]).group(1)

        # Convert the z-component from scientific notation to float
        z_component = float(match[2])

        # Store the z-component in the dictionary
        if part_number in torque_z:
            torque_z[part_number].append(z_component)
        else:
            torque_z[part_number] = [z_component]

# Sort the dictionary by part number
torque_z = dict(sorted(torque_z.items()))

last_12_values = torque_z['1'][-12:]

# Print the formatted output
for i, value in enumerate(last_12_values, start=1):
    print(f"Torque#{i} {value:.6f}")