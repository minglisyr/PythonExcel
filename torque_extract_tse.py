import os
import csv

def get_last_value(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        last_line = lines[-1]
        last_value = last_line.split()[-1]  # Extract the last value
        return last_value

# Base path and folder names
base_path = r'D:\00_ML2954\04_TSE_MODEL\KB30_files'
folder_names = [f'dp{i}' for i in range(35)]

# Initialize lists to store values
values1 = []  # For Torque_on_mvpt1.prb
values2 = []  # For Torque_on_mvpt2.prb

# Iterate through folders
for folder_name in folder_names:
    file_path1 = os.path.join(base_path, folder_name, 'PFL', 'PFL', 'Outputs', 'Torque_on_mvpt1.prb')
    file_path2 = os.path.join(base_path, folder_name, 'PFL', 'PFL', 'Outputs', 'Torque_on_mvpt2.prb')
    
    last_value1 = get_last_value(file_path1)
    last_value2 = get_last_value(file_path2)
    
    values1.append(last_value1)
    values2.append(last_value2)

# Save values to CSV file
output_file = 'torque_values_output.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Folder', 'Torque_on_mvpt1', 'Torque_on_mvpt2'])
    for folder_name, value1, value2 in zip(folder_names, values1, values2):
        writer.writerow([folder_name, value1, value2])

print(f"Values saved to {output_file}")



