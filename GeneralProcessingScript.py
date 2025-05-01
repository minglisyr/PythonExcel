#!/usr/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt

def get_files_in_directory(directory, extensions):
    """Retrieve all files with specified extensions in the directory and subdirectories."""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def main():
    # Ask user for subdirectory name
    subdirectory = input("Enter subdirectory name (default is current directory): ").strip()
    if not subdirectory:
        subdirectory = os.getcwd()
    else:
        subdirectory = os.path.abspath(subdirectory)

    # Check if the directory exists
    if not os.path.exists(subdirectory):
        print(f"Error: The directory '{subdirectory}' does not exist.")
        return

    # Get all .csv, .xls, and .xlsx files
    extensions = ('.csv', '.xls', '.xlsx')
    files = get_files_in_directory(subdirectory, extensions)

    if not files:
        print("No files found with the specified extensions.")
        return

    # Combine all data into a single DataFrame by appending columns
    combined_data = pd.DataFrame()
    for file in files:
        try:
            if file.endswith('.csv'):
                data = pd.read_csv(file)
            else:
                data = pd.read_excel(file)
            
            # Rename columns to include the filename without extension
            filename = os.path.splitext(os.path.basename(file))[0]  # Remove file extension
            data.columns = [f"{col} - {filename}" for col in data.columns]
            
            # Append columns to the combined DataFrame
            combined_data = pd.concat([combined_data, data], axis=1)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    # Provide a summary of the imported data
    print("\nSummary of Combined Data:")
    print(combined_data.info())
    print("\nFirst 5 Rows of Combined Data:")
    print(combined_data.head())

    # Write the combined data to an .xlsx file in the current directory
    output_file = os.path.join(os.getcwd(), 'DataInProcessing.xlsx')
    try:
        combined_data.to_excel(output_file, index=False)
        print(f"\nCombined data has been written to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")

    # Plot all curves in a single plot
    try:
        plt.figure(figsize=(10, 6))
        for file in files:
            if file.endswith('.csv'):
                data = pd.read_csv(file)
            else:
                data = pd.read_excel(file)
            
            # Extract filename without extension
            filename = os.path.splitext(os.path.basename(file))[0]
            
            # Plot each column (Y) against the first column (X)
            x_column = data.columns[0]
            y_columns = data.columns[1:]
            for y_column in y_columns:
                plt.plot(data[x_column], data[y_column], label=f"{y_column} vs {x_column} - {filename}")
        
        # Set x and y labels based on the first two columns of the first file
        first_file = files[0]
        if first_file.endswith('.csv'):
            first_data = pd.read_csv(first_file)
        else:
            first_data = pd.read_excel(first_file)
        plt.xlabel(first_data.columns[0])  # X-axis title
        plt.ylabel(first_data.columns[1])  # Y-axis title

        plt.title("Combined Plot of All Curves")
        plt.legend(loc="best", fontsize="small")
        plt.grid()
        plt.show()
    except Exception as e:
        print(f"Error while plotting data: {e}")

if __name__ == "__main__":
    main()
