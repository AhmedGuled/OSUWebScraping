import requests
from bs4 import BeautifulSoup
import csv
import os

# Set up the URL and output directory
url = 'https://economics.osu.edu/people'
output_dir = "Directories"
csv_filename = os.path.join(output_dir, "Economics_directory.csv")

# Fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all person entries on the page
people_rows = soup.find_all('div', class_='views-field-fieldset')

people_data = []

for person in people_rows:
    name_tag = person.find('span', class_='people-name')  # Extracting name
    title_tag = person.find('div', class_='views-field-field-your-title')  # Extracting title
    email_tag = person.find('div', class_='views-field-mail')  # Extracting email

    if name_tag and title_tag:
        name = name_tag.text.strip()
        title = title_tag.text.strip()

        if 'lecturer' in title.lower() or 'professor' in title.lower():
            if email_tag:
                email_link = email_tag.find("a", href=True)
                email = email_link['href'].replace('mailto:', '').strip() if email_link else "No email found"
            else:
                email = "No email found"

            people_data.append([name, title, email])

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write data to CSV
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])
    writer.writerows(people_data)

print(f"Found {len(people_data)} people matching the criteria.")
print(f"Data has been written to {csv_filename}")
