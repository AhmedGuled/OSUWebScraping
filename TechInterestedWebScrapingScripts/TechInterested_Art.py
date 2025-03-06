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

file_path = './directories/Art_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    email = row['Email']  # Extract email for dot_num

    # Skip if email is missing or invalid
    if pd.isna(email) or type(email) is not str:
        print(f"Skipping {name}: Invalid email")
        continue

    # Extract lastname and dot_num from email
    try:
        email_parts = email.split('@')[0].split('.')
        if len(email_parts) < 2:
            print(f"Skipping {name}: Invalid email format")
            continue
        lastname = email_parts[0]  # Last name before the first dot
        dot_num = email_parts[1]  # Dot number after the first dot
    except IndexError:
        print(f"Skipping {name}: Email format is invalid")
        continue

    # Construct URL using lastname and dot_num
    url = f"https://art.osu.edu/people/{lastname}.{dot_num}"

    # Debugging: Print the URL being processed
    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the specific div
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

# Overwrite the existing file with new results
output_df.to_csv("./TechDirectories/Tech_Interested_Professors_art.csv", index=False, mode='w')

print("Script complete. Results written to Tech_Interested_Professors_art.csv.")
