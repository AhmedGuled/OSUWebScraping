import os
import pandas as pd

# Define the absolute path to the Directories folder
directories_folder = "/Users/jaredalonzo/Documents/OSUWebScraping/Directories"

# Ensure the directory exists
if not os.path.exists(directories_folder):
    print("Error: The specified directory does not exist.")
    exit()

# List all CSV files in the directory
csv_files = [file for file in os.listdir(directories_folder) if file.endswith(".csv")]

# Check if there are CSV files
if not csv_files:
    print("Error: No CSV files found in the directory.")
    exit()

# Create an empty list to store dataframes
dataframes = []

# Read and append each CSV file
for file in csv_files:
    file_path = os.path.join(directories_folder, file)
    try:
        df = pd.read_csv(file_path)
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Concatenate all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Define the output file path
output_file = "/Users/jaredalonzo/Documents/OSUWebScraping/combined_faculty.csv"

# Save the combined CSV file
combined_df.to_csv(output_file, index=False)

print(f"Combined CSV saved as {output_file}")
