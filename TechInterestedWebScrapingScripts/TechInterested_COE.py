import requests
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

file_path = './Directories/COE_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    email = row['Email']

    # Skip if name is missing
    if pd.isna(name):
        continue

    # Handle missing or invalid emails
    if pd.isna(email) or not isinstance(email, str):
        print(f"Skipping {name}: Invalid email")
        dot_num = "1"
    else:
        try:
            dot_num = email.split('.')[-2].split('@')[0]
        except IndexError:
            dot_num = "1"

    # Process name
    name_parts = name.split(',')
    firstname = name_parts[-1].strip().lower()
    lastname = name_parts[0].strip().lower()

    # Clean up last name
    lastname = lastname.rstrip(',')
    lastname = lastname.replace(' ', '').replace("'", "")

    # Construct profile URL
    url = f"https://engineering.osu.edu/people/{lastname}.{dot_num}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            specific_div = soup.find('div', class_='coe-person content-body field-body')
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

# Save results to CSV (overwrite)
output_df = pd.DataFrame(results)
output_df.to_csv("./TechDirectories/Tech_Interested_Professors.csv", index=False, mode='w')

print("Script complete. Results saved to Tech_Interested_Professors.csv.")
