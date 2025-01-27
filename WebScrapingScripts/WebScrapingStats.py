import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url = "https://stat.osu.edu/people"

# Send request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
data = []
people = soup.find_all(class_="views-field-fieldset")

for person in people:
    name_tag = person.find(class_="views-field-field-first-name")
    title_tag = person.find(class_="views-field-field-your-title")
    email_tag = person.find('a', href=True, string=lambda href: "mailto:" in href if href else False)

    name = name_tag.get_text(strip=True) if name_tag else "No name found"
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    email = email_tag['href'].replace("mailto:", "") if email_tag else "No email found"
    
    # Only include lecturers and professors
    if "lecturer" in title.lower() or "professor" in title.lower():
        data.append([name, title, email])

# Write data to CSV
csv_filename = "Statistics_directory.csv"
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Title", "Email"])
    writer.writerows(data)

print(f"Data has been written to {csv_filename}")
