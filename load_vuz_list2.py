import csv
import pathlib

import requests
from bs4 import BeautifulSoup as bs

for n in range(1, 11):
    print(f'Loading page {n}...')
    page = requests.get(f'https://vuzopedia.ru/region/city/59?page={n}')
    page.raise_for_status()

    print('Loaded successfully. Parsing...')
    soup = bs(page.text, 'lxml')
    vuz = []
    divs = soup.find_all('div', class_="vuzesfullnorm")
    prefix = 'https://vuzopedia.ru'
    for d in divs:
        link = d.find('div').find('a')
        vuz.append((link.text.strip(), prefix + link.get('href')))

    print(f'{len(vuz)} found. Saving to file...')
    root = pathlib.Path(__file__).parent
    with open(root / 'vuz.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for x in vuz:
            writer.writerow(x)
