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

file_path = '../Directories/Fisher_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    email = row['Email']

    if pd.isna(email) or not isinstance(email, str):
        print(f"Skipping {name}: Invalid email")
        continue

    try:
        email_parts = email.split('@')[0].split('.')
        if len(email_parts) < 2:
            print(f"Skipping {name}: Invalid email format")
            continue

        lastname = email_parts[0].replace(" ", "").replace("'", "")
        dot_num = email_parts[1]
    except IndexError:
        print(f"Skipping {name}: Email format is invalid")
        continue

    url = f"https://fisher.osu.edu/people/{lastname}.{dot_num}"
    print(f"Checking: {name} | {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            full_text = soup.get_text(separator=' ', strip=True).lower()

            matched_keywords = [kw for kw in keywords if kw.lower() in full_text]

            if matched_keywords:
                print(f"MATCH for {name}: {matched_keywords}")
                results.append({
                    "Name": name,
                    "Profile URL": url,
                    "Keywords Found": ", ".join(matched_keywords)
                })
            else:
                print(f"No match for {name}")
        else:
            print(f"Failed to load {url} (status: {response.status_code})")
    except Exception as e:
        print(f"Error with {url}: {e}")

    if index % 10 == 0:
        print(f"Processed {index} entries...")

output_df = pd.DataFrame(results)
output_df.to_csv("../TechDirectories/Tech_Interested_Professors_fisher.csv", index=False, mode='w')

print("Script complete. Filtered results saved.")
