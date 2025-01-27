import requests
from bs4 import BeautifulSoup
import csv

url = 'https://design.osu.edu/people'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

people_rows = soup.find_all('div', class_='views-field-fieldset')

people_data = []

for person in people_rows:
    name_tag = person.find('a', class_='views-field-field-first-name')
    title_tag = person.find('div', class_='views-field-field-your-title')
    email_tag = person.find('a', href=True, text=True)

    if name_tag and title_tag and ('professor' in title_tag.text.lower() or 'lecturer' in title_tag.text.lower()):
        name = name_tag.text.strip()
        title = title_tag.text.strip()
        email = email_tag['href'].replace('mailto:', '') if email_tag else 'No email found'
        people_data.append([name, title, email])

with open('Design_directory.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email'])
    writer.writerows(people_data)

print(f"Found {len(people_data)} people matching the criteria.")
