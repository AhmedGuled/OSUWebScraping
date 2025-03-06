import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define keywords to search for
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

# File path to input CSV
file_path = './directories/EarthSciences_directory.csv'
professors_data = pd.read_csv(file_path)

results = []
base_url = "https://earthsciences.osu.edu"

# Iterate through each professor entry
for index, row in professors_data.iterrows():
    name = row['Name']
    relative_url = row['Email']  # This column likely contains profile URLs, not emails

    # Ensure relative URL is valid
    if pd.isna(relative_url) or not isinstance(relative_url, str) or not relative_url.startswith('/people/'):
        print(f"Skipping {name}: Invalid profile URL")
        continue

    # Construct the full URL
    full_url = f"{base_url}{relative_url}"

    # Debugging: Print the URL being processed
    print(f"Processing: {full_url}")

    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            specific_div = soup.find('div', class_="col-xs-12 col-sm-9 bio-btm-left")
            if specific_div:
                text_content = specific_div.get_text().lower()
                matched_keywords = [kw for kw in keywords if kw in text_content]
                if matched_keywords:
                    results.append({
                        "Name": name,
                        "Profile URL": full_url,
                        "Keywords Found": ", ".join(matched_keywords)
                    })
            else:
                print(f"Specific div not found for {full_url}")
        else:
            print(f"URL not found: {full_url}")
    except Exception as e:
        print(f"Error with {full_url}: {e}")

    if index % 5 == 0:  # Print progress more frequently
        print(f"Processed {index} entries...")

# Convert results to a DataFrame
output_df = pd.DataFrame(results)

# Save results to CSV
output_file_path = "./TechDirectories/Tech_Interested_Professors_earthsciences.csv"
output_df.to_csv(output_file_path, index=False, mode='w')

print(f"Script complete. Results written to {output_file_path}.")
