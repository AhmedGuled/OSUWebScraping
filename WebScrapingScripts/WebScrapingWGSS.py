import requests
from bs4 import BeautifulSoup
import csv

# URL for the WGSS department
url = "https://wgss.osu.edu/people"
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Error: Unable to access {url}. Status Code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# CSV file setup
filename = "WGSS_directory.csv"
fields = ["Name", "Title", "Email"]
rows = []

# Find all person entries on the page
people_entries = soup.find_all('fieldset', class_='inner-people-grid')

for person in people_entries:
    # Extract the name
    name_tag = person.find('a', class_='views-field-field-first-name')
    name = name_tag.get_text(strip=True) if name_tag else "N/A"
    
    # Extract the title
    title_tag = person.find('div', class_='views-field-field-your-title')
    title = title_tag.get_text(strip=True) if title_tag else "N/A"
    
    # Extract the email
    email_tag = person.find('a', href=lambda href: href and "mailto:" in href)
    email = email_tag['href'].replace("mailto:", "") if email_tag else "N/A"
    
    # Only add faculty members with relevant titles
    if any(word in title.lower() for word in ["professor", "lecturer", "instructor", "faculty"]):
        rows.append([name, title, email])

# Write to CSV
try:
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    print(f"Data has been written to {filename}")
except Exception as e:
    print(f"Error writing to CSV: {e}")
