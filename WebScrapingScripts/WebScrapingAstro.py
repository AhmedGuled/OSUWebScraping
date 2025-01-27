import requests
from bs4 import BeautifulSoup
import csv

url = 'https://astronomy.osu.edu/people'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

people = soup.find_all('div', class_='views-field-fieldset')

filtered_people = []

for person in people:
    name_tag = person.find('a', class_='views-field-field-first-name')
    title_tag = person.find('div', class_='views-field-field-your-title')

    if name_tag and title_tag:
        name = name_tag.text.strip()
        title = title_tag.text.strip()

        if 'lecturer' in title.lower() or 'professor' in title.lower():
            email_tag = person.find('a', href=lambda href: href and 'mailto:' in href)
            if email_tag:
                email = email_tag['href'].replace('mailto:', '').strip()
            else:
                email_tag = person.find('a', href=True)
                if email_tag and '@' in email_tag.text:
                    email = email_tag.text.strip()
                else:
                    email = 'No email found'

            filtered_people.append([name, title, email])

csv_file = 'Astronomy_directory.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])
    writer.writerows(filtered_people)

print(f"Data has been written to {csv_file}")
