import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://aaas.osu.edu/people"

response = requests.get(base_url)

if response.status_code != 200:
    print(f"Stopping: received status code {response.status_code}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')

    people = []

    people_rows = soup.find_all('div', class_='views-field-fieldset')

    print(f"Found {len(people_rows)} people rows")

    for person in people_rows:
        name_tag = person.find('span', class_='people-name')
        title_tag = person.find('div', class_='views-field-field-your-title')
        email_tag = person.find('a', href=lambda href: href and "mailto:" in href)

        name = name_tag.text.strip() if name_tag else "No name found"
        title = title_tag.text.strip() if title_tag else "No title found"
        email = email_tag['href'].replace('mailto:', '').strip() if email_tag else "No email found"

        print(f"Name: {name}, Title: {title}, Email: {email}")

        if "Professor" in title or "Lecturer" in title:
            people.append([name, title, email])

    if people:
        with open('AAAS_directory.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Title', 'Email'])
            writer.writerows(people)

        print("Data has been written to professors.csv")
    else:
        print("No people matching the criteria were found.")
