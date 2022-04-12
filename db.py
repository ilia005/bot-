from contextlib import contextmanager
import sqlite3
import os 

DB_FILE = os.path.join(os.path.dirname(__file__), 'ege.sqlite3')


@contextmanager
def get_cursor() -> sqlite3.Cursor:
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
    try:
        yield cur
    finally:
        cur.close()
        con.commit()
        con.close()
