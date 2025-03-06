import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

# List of keywords to search for in faculty profiles
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

# Input file path containing faculty directory data
file_path = './directories/PoliticalScience_directory.csv'

# Ensure the directory file exists before proceeding
if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found.")
    exit()

# Read the CSV file containing professor names and emails
professors_data = pd.read_csv(file_path)

# List to store results
results = []

for index, row in professors_data.iterrows():
    name = row.get('Name', 'Unknown')
    email = row.get('Email', '')

    # Skip if email is missing or invalid
    if pd.isna(email) or not isinstance(email, str):
        print(f"Skipping {name}: Invalid email")
        continue

    # Extract last name and dot number from email
    try:
        email_parts = email.split('@')[0].split('.')
        lastname = email_parts[0]
        dot_num = email_parts[1]
    except IndexError:
        print(f"Skipping {name}: Email format is invalid")
        continue

    # Construct the faculty profile URL
    url = f"https://polisci.osu.edu/people/{lastname}.{dot_num}"

    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Locate the section containing faculty profile details
            specific_div = soup.find('div', class_="col-xs-12 col-sm-9 bio-btm-left")
            if specific_div:
                text_content = specific_div.get_text().lower()
                matched_keywords = [kw for kw in keywords if kw in text_content]
                if matched_keywords:
                    results.append({
                        "Name": name,
                        "Profile URL": url,
                        "Keywords Found": ", ".join(matched_keywords)
                    })
            else:
                print(f"Specific div not found for {url}")
        else:
            print(f"URL not found: {url}")
    except Exception as e:
        print(f"Error with {url}: {e}")

    if index % 50 == 0:
        print(f"Processed {index} entries...")

# Convert results to a DataFrame
output_df = pd.DataFrame(results)

# Define output file path
output_file = "./TechDirectories/Tech_Interested_Professors_politicalscience.csv"

# Overwrite the CSV file instead of appending
output_df.to_csv(output_file, mode='w', header=True, index=False)

print(f"Script complete. Results written to {output_file}.")
