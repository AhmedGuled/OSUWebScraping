import pandas as pd

# File path
file_path = "/Users/jaredalonzo/Documents/OSUWebScraping/Directories/combined_faculty.csv"

# Load CSV and clean column names
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower()  # Normalize column names

# Strip spaces and ensure emails are lowercase
df['email'] = df['email'].str.strip().str.lower()

# Drop rows where email is missing
df.dropna(subset=['email'], inplace=True)

# Identify duplicate emails
duplicates = df[df.duplicated(subset=['email'], keep=False)]

# Dictionary to store combined titles
combined_titles = {}

for index, row in duplicates.iterrows():
    email = row['email']
    title = row['title']
    
    if email not in combined_titles:
        combined_titles[email] = set()
    combined_titles[email].add(title)

# Update the dataframe
for email, titles in combined_titles.items():
    matching_rows = df[df['email'] == email]
    
    if matching_rows.empty:
        continue  # Skip if email is not found

    first_index = matching_rows.index[0]

    # Combine titles into a single string
    df.at[first_index, 'title'] = "; ".join(sorted(filter(pd.notna, titles)))

    # Drop all but the first occurrence
    df = df.drop(matching_rows.index[1:])

# Save the cleaned data
df.to_csv(file_path, index=False)
print("Duplicates merged and cleaned successfully.")
