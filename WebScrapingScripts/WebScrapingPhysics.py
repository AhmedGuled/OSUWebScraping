import requests
from bs4 import BeautifulSoup
import csv

# URL and CSV file setup
url = "https://physics.osu.edu/people"
csv_filename = "Physics_directory.csv"

# Fetch the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Locate all person entries on the page
people_rows = soup.find_all("div", class_="people-row")

# Open the CSV file for data writing
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Title", "Email"])  # CSV header

    for person in people_rows:
        # Extract and filter the title
        title_tag = person.find("div", class_="views-field-field-your-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if "lecturer" in title.lower() or "professor" in title.lower():
                # Extract name
                name_tag = person.find("a", class_="views-field-field-first-name")
                name = name_tag.get_text(strip=True) if name_tag else "No name found"
                
                # Extract email
                email_tag = person.find("a", href=True, text=lambda text: text and "@" in text)
                email = email_tag.get_text(strip=True) if email_tag else "No email found"
                
                # Write data to CSV
                writer.writerow([name, title, email])

print(f"Data has been written to {csv_filename}")
