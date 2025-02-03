import requests
from bs4 import BeautifulSoup
import pandas as pd

keywords = ["technology", "computing", "AI", "data science", "machine learning", "software", "programming"]

file_path = '/Users/ahmedguled/PythonWebScraping/Directories/COE_directory.csv'
professors_data = pd.read_csv(file_path)

results = []

for index, row in professors_data.iterrows():
    name = row['Name']
    if pd.isna(name):  
        continue
    
    name_parts = name.split()
    if len(name_parts) < 2:
        continue  
    
    lastname = name_parts[-1].lower()
    firstname = name_parts[0].lower()
    url = f"https://engineering.osu.edu/people/{lastname}.1"
    
    print(f"Processing: {url}")  
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text().lower()
            
            matched_keywords = [kw for kw in keywords if kw in text_content]
            if matched_keywords:
                results.append({
                    "Name": name,
                    "Profile URL": url,
                    "Keywords Found": ", ".join(matched_keywords)
                })
        else:
            print(f"URL not found: {url}")
    except Exception as e:
        print(f"Error with {url}: {e}")
        continue

    if index % 50 == 0:
        print(f"Processed {index} entries...")

output_df = pd.DataFrame(results)
output_df.to_csv("/Users/ahmedguled/PythonWebScraping/Directories/Tech_Interested_Professors.csv", index=False)

print("Script complete. Results saved to Tech_Interested_Professors.csv.")
