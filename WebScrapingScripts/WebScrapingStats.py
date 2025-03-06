import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
base_url = "https://stat.osu.edu/people"

# Send request to the website
try:
    response = requests.get(base_url)
    response.raise_for_status()  # Raise an error for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
data = []
people = soup.find_all(class_="views-field-fieldset")  # Each professor's entry

for person in people:
    try:
        # Extract name
        name_tag = person.find('a', href=lambda href: href and "/people/" in href)
        name = name_tag.get_text(strip=True) if name_tag else "No name found"

        # Extract title
        title_tag = person.find(class_="views-field-field-your-title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        # Extract email
        email_tag = person.find('a', href=lambda href: href and "mailto:" in href)
        email = email_tag['href'].replace("mailto:", "") if email_tag else "No email found"

        # Only include lecturers and professors
        if "lecturer" in title.lower() or "professor" in title.lower():
            data.append([name, title, email])
    except Exception as e:
        print(f"Error processing a person: {e}")

# Write data to CSV
csv_filename = "./directories/Statistics_directory.csv"
try:
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Title", "Email"])
        writer.writerows(data)
    print(f"Data has been written to {csv_filename}")
except Exception as e:
    print(f"Error writing to CSV: {e}")