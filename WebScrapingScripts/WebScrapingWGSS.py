import requests
from bs4 import BeautifulSoup
import csv
import os

# URL and directory setup
url = "https://wgss.osu.edu/people"
output_dir = "Directories"
csv_filename = os.path.join(output_dir, "WGSS_directory.csv")

# Fetch the webpage content
try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()  # Check for request errors
    soup = BeautifulSoup(response.text, 'html.parser')
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
    exit()

# Locate all person entries on the page
people_entries = soup.find_all('div', class_='views-field views-field-fieldset')

people_data = []

for person in people_entries:
    try:
        # Extract name
        name_tag = person.find('span', class_='people-name')
        name = name_tag.get_text(strip=True) if name_tag else "No name found"

        # Extract title
        title_tag = person.find('div', class_='views-field views-field-field-your-title')
        title = title_tag.find('div', class_='field-content').get_text(strip=True) if title_tag else "No title found"

        # Extract email
        email_tag = person.find('div', class_='views-field views-field-mail')
        email = email_tag.find('a')['href'].replace("mailto:", "").strip() if email_tag and email_tag.find('a') else "No email found"

        # Filter relevant faculty titles
        if any(word in title.lower() for word in ["professor", "lecturer", "instructor", "faculty", "chair"]):
            people_data.append([name, title, email])

    except Exception as e:
        print(f"Error processing a person: {e}")

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write data to CSV
try:
    with open(csv_filename, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Title", "Email"])  # CSV header
        writer.writerows(people_data)

    print(f"Found {len(people_data)} faculty members matching the criteria.")
    print(f"Data has been written to {csv_filename}")

except Exception as e:
    print(f"Error writing to CSV: {e}")
