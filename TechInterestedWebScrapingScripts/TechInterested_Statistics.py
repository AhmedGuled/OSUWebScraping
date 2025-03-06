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

file_path = './directories/Statistics_directory.csv'

# Ensure input file exists
if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found.")
    exit()

# Read professor directory CSV
professors_data = pd.read_csv(file_path)

# Store results
results = []

for index, row in professors_data.iterrows():
    name = row.get('Name', 'Unknown')
    email = row.get('Email', '')

    # Skip invalid emails
    if pd.isna(email) or not isinstance(email, str):
        print(f"Skipping {name}: Invalid email")
        continue

    # Ensure valid osu.edu email domains
    if not (email.endswith("@osu.edu") or email.endswith("@stat.osu.edu")):
        print(f"Skipping {name}: Email domain is not @osu.edu or @stat.osu.edu")
        continue

    # Extract lastname and dot number from email
    try:
        email_local_part = email.split('@')[0]
        email_parts = email_local_part.split('.')

        if len(email_parts) == 2:  # lastname.dotnum@osu.edu
            lastname, dot_num = email_parts
        else:  # lastname@osu.edu (No dotnum)
            lastname = email_local_part
            dot_num = "1"  # Default dot number if missing

    except Exception as e:
        print(f"Skipping {name}: Error parsing email - {e}")
        continue

    # Construct faculty profile URL
    url = f"https://stat.osu.edu/people/{lastname}.{dot_num}"

    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract canonical URL (fallback to original URL if missing)
            canonical_link = soup.find('link', rel='canonical')
            canonical_url = canonical_link['href'] if canonical_link else url

            # Locate faculty bio section
            specific_div = (
                soup.find('div', class_="col-xs-12 col-sm-9 bio-btm-left") or
                soup.find('div', class_="profile-content") or
                soup.find('div', class_="bio-content") or
                soup.find('div', class_="content-body")
            )

            if specific_div:
                text_content = specific_div.get_text().lower()
                matched_keywords = [kw for kw in keywords if kw in text_content]

                if matched_keywords:
                    results.append({
                        "Name": name,
                        "Profile URL": canonical_url,  # Use canonical URL if available
                        "Keywords Found": ", ".join(matched_keywords)
                    })
            else:
                print(f"No relevant content found for {url}")
        else:
            print(f"URL not found: {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

    # Print progress every 50 entries
    if index % 50 == 0:
        print(f"Processed {index} entries...")

# Convert results to DataFrame
output_df = pd.DataFrame(results)

# Overwrite the CSV file instead of appending
csv_filename = "./TechDirectories/Tech_Interested_Professors_statistics.csv"

try:
    output_df.to_csv(csv_filename, index=False)
    print(f"Script complete. Results written to {csv_filename}.")
except Exception as e:
    print(f"Error writing to CSV: {e}")
