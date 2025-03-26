import pandas as pd

def extract_names(input_file):
    # Open and read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Initialize an empty list to store the strings
    STR = []
    
    # Iterate through the lines to find `[Name]` sections
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("[Name]"):
            # The string after `[Name]` is the name we want to extract
            if i + 1 < len(lines):  # Ensure there is a next line
                name = lines[i + 1].strip()
                STR.append(name)
    
    return STR

def process_csv(file_path, output_path):
    # Read the file line by line
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Initialize variables
    blocks = []
    current_block = []

    # Divide content into blocks based on your predefined structure
    for line in lines:
        if line.strip():  # Non-blank line
            current_block.append(line.strip())
        else:  # Blank line
            if current_block:  # End of a block
                blocks.append(current_block)
                current_block = []
    
    # Add the last block if it exists
    if current_block:
        blocks.append(current_block)

    # Prepare the output DataFrame
    max_rows = max(len(block) for block in blocks)  # Determine the maximum block length
    data = pd.DataFrame(index=range(max_rows))  # Create an empty DataFrame with enough rows

    # Populate the columns based on blocks
    for i, block in enumerate(blocks):
        col_index = i * 3  # Each block occupies three columns (Header, Time, Value)
        header = [block[0]] if len(block) > 0 else ['']
        time_value_pairs = [line.split(',') for line in block[1:]]

        # Extract time and value pairs into separate columns
        times = [pair[0].strip() if len(pair) > 1 else '' for pair in time_value_pairs]
        values = [pair[1].strip() if len(pair) > 1 else '' for pair in time_value_pairs]

        # Add columns to the DataFrame
        data.insert(col_index, f'Header_{i + 1}', pd.Series(header + [''] * (max_rows - len(header))))
        data.insert(col_index + 1, f'Time_{i + 1}', pd.Series(times + [''] * (max_rows - len(times))))
        data.insert(col_index + 2, f'Value_{i + 1}', pd.Series(values + [''] * (max_rows - len(values))))

    # Save the processed DataFrame to a new CSV file
    data.to_csv(output_path, index=False)

# Example usage:
process_csv('test.csv', 'processed_test.csv')

def unitConvert_csv(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file, header=None)  # Read without assuming headers
    
    # Extract headers from the first two rows and combine them
    headers = (df.iloc[0].fillna('') + " " + df.iloc[1].fillna('')).str.strip()  # Ensure headers are strings and remove extra spaces
    
    # Extract data rows starting from row index 2
    data = df.iloc[2:].reset_index(drop=True)
    
    # Process each column based on its type (Time or Value)
    processed_data = pd.DataFrame()

    for column in data.columns:
        column_header = str(headers[column])  # Ensure the header is treated as a string
        if "Time" in column_header:
            # Divide Time [s] values by 60 to convert to minutes and round to 2 decimals
            processed_data[column_header] = (pd.to_numeric(data[column], errors='coerce') / 60).round(2)
        elif "Value" in column_header:
            # Subtract temperature values by 273 and round to 2 decimals
            processed_data[column_header] = (pd.to_numeric(data[column], errors='coerce') - 273).round(2)
    
    # Save the processed data to a new CSV file
    processed_data.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")

# Example usage:
unitConvert_csv('processed_test.csv', 'unitConverted_test.csv')

def process_columns(input_path, output_path):
    # Load the processed CSV into a DataFrame
    df = pd.read_csv(input_path)

    # Initialize a list to store the indices of columns to keep
    cols_to_keep = []
    i = 0

    # Loop through columns in chunks of 4 (2 to delete + 2 to keep)
    while i < df.shape[1]:
        # Skip the first 2 columns in the chunk
        i += 2
        # Add the next 2 columns (if they exist) to the list of columns to keep
        if i < df.shape[1]:
            cols_to_keep.extend(range(i, min(i + 2, df.shape[1])))
        # Move to the next chunk
        i += 2

    # Keep only the selected columns
    df = df.iloc[:, cols_to_keep]

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"Processed file saved as: {output_path}")

# Example usage:
process_columns('unitConverted_test.csv', 'final_processed_test.csv')

# Convert and save as XLSX
df = pd.read_csv('final_processed_test.csv')

# df = df.drop(index=0)

# Replace all 'Time_*' column names with 'Time [s]'
df.columns = [col if not col.startswith('Time_') else 'Time [s]' for col in df.columns]

# Replace all 'Value_*' column names with STR[0], STR[1], etc.
value_columns = [col for col in df.columns if col.startswith('Value_')]
STR = extract_names('test.csv')

for i, col in enumerate(value_columns):
    df.rename(columns={col: STR[i]}, inplace=True)

# Rename columns for easier manipulation
df.columns = [
    'Time [s]', 'Max Temp Case Elevated MaxT',
    'Time [s].1', 'Max Temp Case Worst MaxT',
    'Time [s].2', 'Min Temp Case Elevated MinT',
    'Time [s].3', 'Min Temp Case Worst MinT',
    'Time [s].4', 'Max Temp Case Lowered MaxT',
    'Time [s].5', 'Min Temp Case Lowered MinT'
]

# Rename the time columns to Time [min], temperature columns to match the new names
df.columns = [
    'Time [min]', 'MaxT @Elevated [C]',
    'Time [min]', 'MaxT @Nominal [C]',
    'Time [min]', 'MinT @Elevated [C]',
    'Time [min]', 'MinT @Nominal [C]',
    'Time [min]', 'MaxT @Lowered [C]',
    'Time [min]', 'MinT @Lowered [C]'
]

# Save the modified DataFrame to a new Excel file
output_file_path = 'final_processed_test_modified.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Modified data saved to {output_file_path}")
