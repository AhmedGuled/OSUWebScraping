import requests
from bs4 import BeautifulSoup
import csv
import os

# Set up the URL and output directory
url = "https://history-of-art.osu.edu/people"
output_dir = "Directories"
csv_filename = os.path.join(output_dir, "History_of_Art_directory.csv")

# Fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all person entries on the page
people_rows = soup.find_all("div", class_="views-field-fieldset")

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the CSV file to write data
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Title", "Email"])  # CSV header

    for person in people_rows:
        # Extract title and filter for 'lecturer' or 'professor'
        title_tag = person.find("div", class_="views-field-field-your-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if "lecturer" in title.lower() or "professor" in title.lower():
                # Extract name
                name_tag = person.find("span", class_="people-name")
                name = name_tag.get_text(strip=True) if name_tag else "No name found"
                
                # Extract email
                email_tag = person.find("div", class_="views-field-mail")
                if email_tag:
                    email_link = email_tag.find("a", href=True)
                    email = email_link['href'].replace('mailto:', '').strip() if email_link else "No email found"
                else:
                    email = "No email found"
                
                # Write data to CSV
                writer.writerow([name, title, email])

print(f"Data has been written to {csv_filename}")
