import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

# Define keywords to search for
keywords = [
    "technology", "computing", "AI", "data science", "machine learning", "software", "programming",
    "artificial intelligence", "big data", "cloud computing", "cybersecurity", "IoT", "blockchain",
    "quantum computing", "robotics", "computer vision", "natural language processing", "augmented reality",
    "virtual reality", "high-performance computing", "data mining", "predictive analytics", "data visualization",
    "statistical modeling", "deep learning", "neural networks", "reinforcement learning", "pattern recognition",
    "software engineering", "web development", "mobile applications", "open source", "API development", 
    "embedded systems", "operating systems", "autonomous systems", "control systems", "signal processing", 
    "networking", "5G", "bioinformatics", "computational biology", "digital health", "data", "user interface"
]

# File path to input CSV
file_path = './directories/Economics_directory.csv'

# Ensure the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

professors_data = pd.read_csv(file_path)

results = []
base_url = "https://economics.osu.edu/people"

# Iterate through each professor entry
for index, row in professors_data.iterrows():
    name = row['Name']
    raw_email = row['Email'] if pd.notna(row['Email']) else "N/A"

    # Skip if email is missing or invalid
    if pd.isna(raw_email) or "@" not in raw_email:
        print(f"Skipping {name}: Invalid email")
        continue

    # Extract lastname and dotnum from email
    try:
        email_parts = raw_email.split('@')[0].split('.')
        lastname = email_parts[0]  # Lastname is before the first dot
        dot_num = email_parts[1] if len(email_parts) > 1 and email_parts[1].isdigit() else "1"  # Dotnum
    except IndexError:
        print(f"Skipping {name}: Email format is invalid")
        continue

    # Construct the correct faculty profile URL
    profile_url = f"{base_url}/{lastname}.{dot_num}"

    # Debugging: Print the URL being processed
    print(f"Processing: {profile_url}")

    try:
        response = requests.get(profile_url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            specific_div = soup.find('div', class_="col-xs-12 col-sm-9 bio-btm-left")
            if not specific_div:
                specific_div = soup.find('div', class_="bio-content")  # Alternative div

            if specific_div:
                text_content = specific_div.get_text().lower()
                matched_keywords = [kw for kw in keywords if kw in text_content]
                if matched_keywords:
                    results.append({
                        "Name": name,
                        "Profile URL": profile_url,
                        "Keywords Found": ", ".join(matched_keywords)
                    })
            else:
                print(f"Specific div not found for {profile_url}")
        else:
            print(f"URL not found: {profile_url}")
    except Exception as e:
        print(f"Error with {profile_url}: {e}")

    if index % 5 == 0:  # Print progress more frequently
        print(f"Processed {index} entries...")

# Convert results to a DataFrame
output_df = pd.DataFrame(results)

# Save results to CSV (overwrite instead of append)
output_file_path = "./TechDirectories/Tech_Interested_Professors_economics.csv"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

output_df.to_csv(output_file_path, index=False)

print(f"Script complete. Results written to {output_file_path}.")
