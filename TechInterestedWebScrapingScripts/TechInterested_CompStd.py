import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

# List of technology-related keywords
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

# **FIXED FILE PATH**
file_path = './directories/ComparativeStudies_directory.csv'

# Ensure file exists before reading
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    raw_email = row['Email'] if pd.notna(row['Email']) else "N/A"
    dot_num = "1"  # Default dot number

    if pd.isna(name):
        continue

    # Handle names that may be in "Last, First" format
    name_parts = name.split(',')
    if len(name_parts) > 1:
        last_name = name_parts[0].strip().lower()  # Extract last name
    else:
        last_name = name.split()[-1].strip().lower()  # Extract last word (last name)

    # Clean up last names (handle hyphens and apostrophes)
    last_name = last_name.replace(" ", "").replace("'", "").replace("-", "")

    # Extract correct dot number from email
    if "@" in raw_email and "." in raw_email:
        email_parts = raw_email.split("@")[0].split(".")
        if len(email_parts) > 1 and email_parts[-1].isdigit():
            dot_num = email_parts[-1]  # Get last numeric part (dot number)

    # Construct correct profile URL
    url = f"https://comparativestudies.osu.edu/people/{last_name}.{dot_num}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            specific_div = soup.find('div', class_="col-xs-12 col-sm-9 bio-btm-left")

            # Alternative div in case structure has changed
            if not specific_div:
                specific_div = soup.find('div', class_="bio-content")

            if specific_div:
                text_content = specific_div.get_text().lower()
                matched_keywords = [kw for kw in keywords if kw in text_content]
            else:
                text_content = ""  # No description found
                matched_keywords = []

            # If no match in bio, check job title
            if not matched_keywords:
                title_text = row['Title'].lower() if pd.notna(row['Title']) else ""
                matched_keywords = [kw for kw in keywords if kw in title_text]

            if matched_keywords:
                results.append({
                    "Name": name,
                    "Profile URL": url,
                    "Keywords Found": ", ".join(matched_keywords)
                })
            else:
                print(f"No match found for {url}")

        else:
            print(f"URL not found: {url}")

    except Exception as e:
        print(f"Error with {url}: {e}")

    if index % 50 == 0:
        print(f"Processed {index} entries...")

# Convert results to a DataFrame
output_df = pd.DataFrame(results)

# Overwrite the file instead of appending
output_file = "./TechDirectories/Tech_Interested_Professors_CompStd.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

output_df.to_csv(output_file, index=False)

print("Script complete. Results saved to Tech_Interested_Professors_CompStd.csv.")
