import requests
from bs4 import BeautifulSoup
import csv
import os

# URL and directory setup
url = "https://sppo.osu.edu/people"
output_dir = "Directories"
csv_filename = os.path.join(output_dir, "SPPO_directory.csv")

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Locate all person entries on the page
people_rows = soup.find_all("div", class_="people-row")

people_data = []

for person in people_rows:
    # Extract name
    name_tag = person.find("span", class_="people-name")
    name = name_tag.get_text(strip=True) if name_tag else "No name found"

    # Extract title
    title_tag = person.find("div", class_="views-field-field-your-title")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Extract email
    email_tag = person.find("div", class_="views-field-mail")
    if email_tag:
        email_link = email_tag.find("a", href=True)
        email = email_link['href'].replace('mailto:', '').strip() if email_link else "No email found"
    else:
        email = "No email found"

    # Filter only professors and lecturers
    if "lecturer" in title.lower() or "professor" in title.lower():
        people_data.append([name, title, email])

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write data to CSV
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Title", "Email"])  # CSV header
    writer.writerows(people_data)

print(f"Found {len(people_data)} people matching the criteria.")
print(f"Data has been written to {csv_filename}")
