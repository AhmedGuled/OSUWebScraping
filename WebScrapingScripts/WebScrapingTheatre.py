import requests
from bs4 import BeautifulSoup
import csv

# URL for the Theatre department
url_theatre = "https://theatreandfilm.osu.edu/people"
response_theatre = requests.get(url_theatre)
soup_theatre = BeautifulSoup(response_theatre.text, 'html.parser')

# CSV file setup for Theatre
filename_theatre = "Theatre_directory.csv"
fields_theatre = ["Name", "Title", "Email"]
rows_theatre = []

# Find all person entries on the page
people_entries_theatre = soup_theatre.find_all('fieldset', class_='inner-people-grid')

for person in people_entries_theatre:
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
        rows_theatre.append([name, title, email])

# Write to CSV
with open(filename_theatre, 'w', newline='') as csvfile_theatre:
    csvwriter_theatre = csv.writer(csvfile_theatre)
    csvwriter_theatre.writerow(fields_theatre)
    csvwriter_theatre.writerows(rows_theatre)

print(f"Data has been written to {filename_theatre}")
