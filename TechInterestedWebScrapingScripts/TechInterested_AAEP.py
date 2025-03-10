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

file_path = './directories/AAAS_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    email = row['Email']  # if email is N/A handle dotnum
    dot_num = email.split('.')[-2].split('@')[0] if type(email) is not float else 1
    # float object has no attribute split???? why is email a float
    if type(email) is float:
        print('found float', name)
    if pd.isna(name):
        continue

    name_parts = name.split(',')
    # if len(name_parts) < 2:
    #     continue

    firstname = name_parts[-1].strip().lower()  # Clean up first name
    lastname = name_parts[0].strip().lower()  # Clean up last name

    # Remove spaces and special characters from last name
    lastname = lastname.replace(' ', '').replace('\'', '')

    # Construct URL using only lastname and dot_num
    url = f"https://aaas.osu.edu/people/{lastname}.{dot_num}"

    # print(f"Processing: {url}")

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
            print(f"URL not found: {url}", lastname)  # what's difference between 56 and 58
            # verify they actually are gone
    except Exception as e:
        print(f"Error with {url}: {e}")  # assume they are gone

    if index % 50 == 0:
        print(f"Processed {index} entries...")

# Convert results to a DataFrame
output_df = pd.DataFrame(results)

# Check if the file already exists
file_exists = os.path.isfile("./Directories/Tech_Interested_Professors_AAAS.csv")

# Append results to the CSV file
if file_exists:
    # If the file exists, append without writing the header
    output_df.to_csv("./Directories/Tech_Interested_Professors_AAAS.csv", mode='a', header=False, index=False)
else:
    # If the file doesn't exist, create it with headers
    output_df.to_csv("./Directories/Tech_Interested_Professors_AAAS.csv", index=False)

print("Script complete. Results appended to Tech_Interested_Professors_AAAS.csv.")