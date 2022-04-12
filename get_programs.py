import csv
import pathlib
from pprint import pprint
import re

from datatypes import College, Program
from utils import format_declension, parse_request, get_fitting_programs


def load_colleges():
    colleges = []
    root = pathlib.Path(__file__).parent
    with open(root / 'vuz.csv', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile)
        for vuzname, vuz_link in reader:
            n = vuz_link.split('/')[-1]
            colleges.append(College(int(n), vuzname, vuz_link))
    return colleges


def load_programs(colleges):
    programs = []
    root = pathlib.Path(__file__).parent
    for c in colleges:
        filename = f'vuz{c.id}.csv'
        with open(root / filename, encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for name, link, subjects, score in reader:
                subjects = set(re.split('[,/]\s*', subjects))
                if not score:
                    continue
                programs.append(Program(0, c, name, link, subjects, int(score)))
    return programs


def handle_request(message_text, programs):
    subs = parse_request(message_text)
    return get_fitting_programs(subs, programs)


print(handle_request('математика 80 русский 70 информатика 99', load_programs(load_colleges())))
