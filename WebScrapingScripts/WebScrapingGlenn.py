import requests
from bs4 import BeautifulSoup
import csv

# URL for the Glenn College directory
url = 'https://glenn.osu.edu/directory'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all directory entries
people = soup.find_all('tr', class_='directory__row')

filtered_people = []

for person in people:
    name_tag = person.find('a', class_='directory__name-title')
    title_tag = person.find('span', class_='directory__name-sub')
    email_tag = person.find('a', class_='directory__email')

    if name_tag and title_tag:
        name = name_tag.text.strip()
        title = title_tag.text.strip()

        if 'lecturer' in title.lower() or 'professor' in title.lower():
            email = email_tag.text.strip() if email_tag else 'No email found'
            filtered_people.append([name, title, email])

# Save results to CSV
csv_file = 'Glenn_directory.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])
    writer.writerows(filtered_people)

print(f"Data has been written to {csv_file}")
