import concurrent.futures
import csv
import os
import pathlib
import re

import requests
from bs4 import BeautifulSoup as bs


class EgeNotFound(Exception):
    pass


def filter_not_printable(text):
    return ''.join(x for x in text if x.isprintable())


def get_spec_info(spec):
    a = spec.find('a', class_='spectittle')
    try:
        ege = spec.find('div', class_='egeInVuzProg').text.strip().removeprefix('ЕГЭ: ')
    except AttributeError as e:
        raise EgeNotFound() from e
    score = re.findall('\d+', spec.find_all('a', class_='tooltipq')[2].text)
    score = score[0] if score else ''
    return [filter_not_printable(a.text), a.get('href'), ege, score]


def get_info_from_page(page):
    for spec in page.find_all('div', class_="itemSpecAll"):
        try:
            yield get_spec_info(spec)
        except EgeNotFound:
            break


def load_vuz_data(vuz_link):
    vuz_link += '/programs/bakispec'
    page = requests.get(vuz_link)
    soup = bs(page.text, 'lxml')
    yield from get_info_from_page(soup)

    try:
        pages_links = [a.get('href') for a in soup.find('ul', class_='pagination').find_all('a')][:-1]
    except AttributeError:
        return

    for link in pages_links:
        print(link)
        page = requests.get(link)
        soup = bs(page.text, 'lxml')
        yield from get_info_from_page(soup)


def get_colledges():
    root = pathlib.Path(__file__).parent
    with open(root / 'vuz.csv', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile)
        for vuzname, vuz_link in reader:
            n = vuz_link.split('/')[-1]
            filename = root / f'vuz{n}.csv'
            if filename.exists():
                continue
            yield filename, vuz_link


def get_programs(args):
    filename, vuz_link = args
    with open(filename, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(load_vuz_data(vuz_link))


vuz = list(get_colledges())
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(get_programs, vuz)
