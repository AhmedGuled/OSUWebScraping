import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://engineering.osu.edu/directory"
page = 0

filter_titles = ['Lecturer', 'Professor', 'Assistant Professor']

with open('osu_directory.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Email', 'Office'])

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Stopping: received status code {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        directory_items = soup.find_all('article', class_='directory-item')

        if not directory_items:
            print(f"No more directory items found on page {page}.")
            break

        for item in directory_items:
            name = item.find('h2', class_='directory-grid-name').get_text(strip=True) if item.find('h2', class_='directory-grid-name') else 'N/A'
            title_div = item.find('div', class_='field-block-node-coe-person-field-appointments')
            title = title_div.get_text(strip=True) if title_div else 'N/A'
            email_div = item.find('div', class_='directory-grid-email')
            email = email_div.get_text(strip=True) if email_div else 'N/A'
            office_div = item.find('div', class_='directory-grid-address')
            office = office_div.get_text(strip=True) if office_div else 'N/A'

           
            if any(keyword in title for keyword in filter_titles):
                writer.writerow([name, title, email, office])

        print(f"Finished page {page}")
        page += 1
        time.sleep(1) 

print("Scraping complete!")