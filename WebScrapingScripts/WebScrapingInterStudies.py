import requests
from bs4 import BeautifulSoup
import csv

# Set up the URL and CSV filename
url = "https://internationalstudies.osu.edu/people"
csv_filename = "InternationalStudies_directory.csv"

# Fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all person entries on the page
people_rows = soup.find_all("div", class_="people-row")

# Open the CSV file to write data
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Title", "Email"])  # CSV header

    for person in people_rows:
        # Extract the title and filter based on 'lecturer' or 'professor'
        title_tag = person.find("div", class_="views-field-field-your-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if "lecturer" in title.lower() or "professor" in title.lower():
                # Extract the name
                name_tag = person.find("a", class_="views-field-field-first-name")
                name = name_tag.get_text(strip=True) if name_tag else "No name found"
                
                # Extract the email
                email_tag = person.find("a", href=True, text=lambda text: text and "@" in text)
                email = email_tag.get_text(strip=True) if email_tag else "No email found"
                
                # Write the data to CSV
                writer.writerow([name, title, email])

print(f"Data has been written to {csv_filename}")
