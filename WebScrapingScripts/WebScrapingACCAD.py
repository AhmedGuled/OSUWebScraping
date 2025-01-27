import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://accad.osu.edu/people"
response = requests.get(base_url)

if response.status_code != 200:
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

with open('accad_professors.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])

    people_items = soup.find_all('div', class_='views-field-fieldset')

    for person in people_items:
        name_tag = person.find('a', class_='views-field-field-first-name')
        title_tag = person.find('div', class_='views-field-field-your-title')
        email_tag = person.find('a', href=True, string=True)

        name = name_tag.text.strip() if name_tag else 'No name'
        title = title_tag.text.strip() if title_tag else 'No title'
        email = email_tag.string.strip() if email_tag else 'No email'

        if any(keyword in title.lower() for keyword in ['professor', 'lecturer']):
            writer.writerow([name, title, email])
