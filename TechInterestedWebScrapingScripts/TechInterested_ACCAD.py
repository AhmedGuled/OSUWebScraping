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

file_path = './directories/ACCAD_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    raw_email = row['Email']  # This is just a name, not an actual email
    dot_num = "1"  # Default dot number if unknown

    if pd.isna(name):
        continue

    name_parts = name.split()
    if len(name_parts) < 2:
        print(f"Skipping entry with no last name: {name}")
        continue

    first_name = name_parts[0].strip().lower()
    last_name = name_parts[-1].strip().lower()

    # Handle special characters in last names
    last_name = last_name.replace(" ", "").replace("'", "").replace("-", "")

    # Generate OSU email format (lastname.#@osu.edu)
    if "." in raw_email:
        dot_num = raw_email.split(".")[-1]  # Extract number if present
    else:
        dot_num = "1"  # Assume default dot number

    # Construct correct profile URL
    url = f"https://accad.osu.edu/people/{last_name}.{dot_num}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
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

# Save results to CSV (overwrite instead of append)
output_df = pd.DataFrame(results)

output_df.to_csv("./TechDirectories/Tech_Interested_Professors_ACCAD.csv", mode='w', index=False)

print("Script complete. Results saved to Tech_Interested_Professors_ACCAD.csv.")
