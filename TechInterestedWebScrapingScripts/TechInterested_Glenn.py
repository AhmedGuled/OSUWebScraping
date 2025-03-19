import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

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

file_path = '../Directories/Glenn_directory.csv'

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()

try:
    professors_data = pd.read_csv(file_path)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
    exit()
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

results = []

for index, row in professors_data.iterrows():
    name = row.get('Name', '').strip()
    email = row.get('Email', '').strip()

    if not name or not email:
        continue

    try:
        name_parts = name.split(", ")
        if len(name_parts) == 2:
            first_name, last_name = name_parts[1], name_parts[0]
        else:
            first_name, last_name = name, ""

        profile_name = f"{first_name} {last_name}".strip().lower().replace(" ", "-")
        url = f"https://glenn.osu.edu/{profile_name}"
    except Exception:
        continue

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            matched_keywords = [kw for kw in keywords if kw in page_text]

            if matched_keywords:
                results.append({
                    "Name": name,
                    "Profile URL": url,
                    "Keywords Found": ", ".join(set(matched_keywords))
                })
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        continue

    if index % 50 == 0:
        print(f"Processed {index} entries...")

output_df = pd.DataFrame(results)

output_dir = "../TechDirectories"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/Tech_Interested_Professors_Glenn.csv"

output_df.to_csv(output_file, index=False)

print(f"Script complete. Results saved to {output_file}.")
