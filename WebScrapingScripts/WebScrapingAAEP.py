import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://aaep.osu.edu/people'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

people = soup.find_all('div', class_='views-field-fieldset')

filtered_people = []

for person in people:
    name_tag = person.find('span', class_='people-name')  # Extracting name
    title_tag = person.find('div', class_='views-field-field-your-title')  # Extracting title

    if name_tag and title_tag:
        name = name_tag.text.strip()
        title = title_tag.text.strip()

        if 'lecturer' in title.lower() or 'professor' in title.lower():
            email_tag = person.find('div', class_='views-field-mail')  # Email is within this div
            if email_tag:
                email_link = email_tag.find('a', href=True)
                if email_link:
                    email = email_link['href'].replace('mailto:', '').strip()
                else:
                    email = 'No email found'
            else:
                email = 'No email found'

            filtered_people.append([name, title, email])

# Ensure the directory exists
output_dir = 'Directories'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_file = os.path.join(output_dir, 'AAEP_directory.csv')
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])
    writer.writerows(filtered_people)

print(f"Data has been written to {csv_file}")
