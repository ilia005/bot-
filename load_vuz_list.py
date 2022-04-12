import csv
import pathlib

import requests
from bs4 import BeautifulSoup as bs

page = requests.get('https://vuzopedia.ru/rate/region/city/59')
soup = bs(page.text, 'lxml')

divs = soup.find_all('div', class_="vuzRateOpiton")
divs = divs[::2]
prefix = 'https://vuzopedia.ru'
vuz = []
for d in divs:
    link = d.find('a')
    vuz.append((link.text, prefix + link.get('href')))

root = pathlib.Path(__file__).parent
with open(root / 'vuz.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for x in vuz:
        writer.writerow(x)
