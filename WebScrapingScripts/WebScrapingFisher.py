import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://fisher.osu.edu/directory"
page = 0

filter_titles = ['Lecturer', 'Professor', 'Assistant Professor']

with open('fisher_directory.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Department', 'Email', 'Phone'])

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Stopping: received status code {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        people = soup.find_all(class_='person-item')

        if not people:  
            print("No more people found, ending scrape.")
            break

        for person in people:
            name = person.find(class_='first-name').text + " " + person.find(class_='last-name').text
            title = person.find(class_='title').text.strip()
            department = person.find(class_='department').text.strip() if person.find(class_='department') else ''
            email = person.find('a', class_='email').get('href').replace('mailto:', '') if person.find('a', class_='email') else ''
            phone = person.find('a', class_='phone').text.strip() if person.find('a', class_='phone') else ''

            if any(keyword in title for keyword in filter_titles):
                writer.writerow([name, title, department, email, phone])

        print(f"Scraped page {page + 1}")
        page += 1
        time.sleep(1)  

print("Scraping complete!")
