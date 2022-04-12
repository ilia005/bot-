import os

from datatypes import subjects
from get_programs import load_colleges, load_programs
from db import DB_FILE, get_cursor

os.remove(DB_FILE)

with get_cursor() as cur:
    print('Creating database')
    cur.executescript(open('init.sql').read())
    cur.executemany('INSERT INTO subjects (subject_name) VALUES (?)', [(s,) for s in subjects])
    cur.execute('SELECT subject_name, subject_id FROM subjects')
    subjects = dict(cur.fetchall())

    print('Loading colleges data')
    colleges = load_colleges()
    for c in colleges:
        print(c)
        cur.execute('INSERT INTO colleges (college_name, college_link) VALUES (?, ?)', (c.name, c.link))
        cur.execute('SELECT college_id FROM colleges WHERE college_name=(?)', (c.name,))
        progs = load_programs([c])
        c.id = cur.fetchone()[0]
        for p in progs:
            cur.execute(
                'INSERT INTO programs (program_name, program_link, score, additional, college_id) VALUES (?, ?, ?, ?, ?)',
                (p.name, p.link, p.score, p.additional, c.id)
            )
            cur.execute('SELECT program_id FROM programs WHERE program_link=(?)', (p.link,))
            p_id = cur.fetchone()[0]
            cur.executemany(
                'INSERT INTO subjects_for_program (subject_id, program_id) VALUES (?, ?)',
                [(subjects[s], p_id) for s in p.subjects]
            )


# test
print(subjects)
with get_cursor() as cur:
    other = set(subjects.values())
    for s in ['математика', 'информатика', 'русский']:
        other.remove(subjects[s])
    placeholder = ', '.join(['?'] * len(other))
    cur.execute(
        f'SELECT * FROM programs WHERE program_id NOT IN \
        (SELECT program_id FROM subjects_for_program WHERE subject_id in ({placeholder}))\
        AND score < 200', tuple(other)
    )
    print(cur.fetchall())
