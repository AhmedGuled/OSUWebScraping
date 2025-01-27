import requests
from bs4 import BeautifulSoup
import csv

# URL for the WGSS department
url = "https://wgss.osu.edu/people"
response = requests.get(url)
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
    name = name_tag.get_text(strip=True) if name_tag else "No name found"
    
    # Extract the title
    title_tag = person.find('div', class_='views-field-field-your-title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    
    # Extract the email
    email_tag = person.find('a', href=lambda href: href and "mailto:" in href)
    email = email_tag['href'].replace("mailto:", "") if email_tag else "No email found"
    
    # Only add professors and lecturers to the rows
    if "professor" in title.lower() or "lecturer" in title.lower():
        rows.append([name, title, email])

# Write to CSV
with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)

print(f"Data has been written to {filename}")
