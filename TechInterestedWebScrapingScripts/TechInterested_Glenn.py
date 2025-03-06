import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

# Define tech-related keywords
keywords = [
    "technology", "computing", "AI", "data science", "machine learning", "software", "programming",
    "artificial intelligence", "big data", "cloud computing", "cybersecurity", "IoT", "blockchain",
    "quantum computing", "robotics", "computer vision", "natural language processing", "augmented reality",
    "virtual reality", "high-performance computing", "data mining", "predictive analytics", "data visualization",
    "statistical modeling", "deep learning", "neural networks", "reinforcement learning", "pattern recognition",
    "software engineering", "web development", "mobile applications", "open source", "API development", 
    "embedded systems", "operating systems", "autonomous systems", "control systems", "signal processing", 
    "networking", "5G", "bioinformatics", "computational biology", "digital health", "data"
]

# Input CSV file with faculty names and emails
file_path = './directories/Glenn_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    email = row['Email']

    if pd.isna(email) or not isinstance(email, str):
        print(f"Skipping {name}: Invalid email")
        continue

    try:
        name_parts = name.split(", ")
        if len(name_parts) == 2:
            first_name, last_name = name_parts[1], name_parts[0]
        else:
            first_name, last_name = name, ""

        profile_name = f"{first_name} {last_name}".strip().lower().replace(" ", "-")
        url = f"https://glenn.osu.edu/people/{profile_name}"  # Fixed URL structure
    except Exception:
        print(f"Skipping {name}: Error constructing URL")
        continue

    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all text from the page
            page_text = soup.get_text().lower()
            matched_keywords = [kw for kw in keywords if kw in page_text]

            if matched_keywords:
                results.append({
                    "Name": name,
                    "Profile URL": url,
                    "Keywords Found": ", ".join(matched_keywords)
                })
        else:
            print(f"URL not found: {url}")
    except Exception as e:
        print(f"Error with {url}: {e}")

    if index % 50 == 0:
        print(f"Processed {index} entries...")

# Convert to DataFrame
output_df = pd.DataFrame(results)

# Ensure directory exists
os.makedirs("TechDirectories", exist_ok=True)
output_file = "./TechDirectories/Tech_Interested_Professors_Glenn.csv"

# Overwrite the existing file instead of appending
output_df.to_csv(output_file, index=False, mode='w')

print("Script complete. Results written to Tech_Interested_Professors_Glenn.csv.")
