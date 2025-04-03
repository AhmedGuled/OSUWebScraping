import os
import pandas as pd

# Path to the TechDirectories folder
tech_dir_folder = "/Users/jaredalonzo/Documents/OSUWebScraping/TechDirectories"

# Ensure the directory exists
if not os.path.exists(tech_dir_folder):
    print("Error: The specified directory does not exist.")
    exit()

# Get all CSV files
csv_files = [file for file in os.listdir(tech_dir_folder) if file.endswith(".csv")]

if not csv_files:
    print("Error: No CSV files found in the directory.")
    exit()

dataframes = []

for file in csv_files:
    file_path = os.path.join(tech_dir_folder, file)
    try:
        # Skip empty files
        if os.path.getsize(file_path) == 0:
            print(f"Skipping {file}: File is empty")
            continue

        df = pd.read_csv(file_path)
        df.columns = [col.strip() for col in df.columns]  # Normalize column names

        if "First Name" in df.columns and "Last Name" in df.columns:
            df["__FullName__"] = df["First Name"].astype(str).str.strip() + " " + df["Last Name"].astype(str).str.strip()
        elif "Name" in df.columns:
            df["__FullName__"] = df["Name"].astype(str).str.strip()
        else:
            print(f"Skipping {file}: No recognizable name columns")
            continue

        dataframes.append(df)

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Combine and deduplicate
combined_df = pd.concat(dataframes, ignore_index=True)
deduplicated_df = combined_df.drop_duplicates(subset="__FullName__")

# Drop the helper column safely
deduplicated_df = deduplicated_df.drop(columns=["__FullName__"])

# Save output
output_path = os.path.join(tech_dir_folder, "combined_unique_faculty_by_fullname.csv")
deduplicated_df.to_csv(output_path, index=False)

print(f"Deduplicated file saved at: {output_path}")
