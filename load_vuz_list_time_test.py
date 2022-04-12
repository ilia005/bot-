import csv
import pathlib
import time

import requests
from bs4 import BeautifulSoup as bs

print(f'Loading page...')
start = time.process_time()
page = requests.get(f'https://vuzopedia.ru/region/city/59')
page.raise_for_status()
end = time.process_time()

print(f'Loaded successfully in {end - start} sec. Parsing...')
start = time.process_time()
soup = bs(page.text, 'lxml')
vuz = []
divs = soup.find_all('div', class_="vuzesfullnorm")
prefix = 'https://vuzopedia.ru'
for d in divs:
    link = d.find('div').find('a')
    vuz.append((link.text.strip(), prefix + link.get('href')))
end = time.process_time()

print(f'{len(vuz)} found in {end - start} sec. Saving to file...')
start = time.process_time()
root = pathlib.Path(__file__).parent
with open(root / 'vuz_test.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for x in vuz:
        writer.writerow(x)
end = time.process_time()
print(f'Wrote in {end - start} sec.')
