import random
import sqlite3
from datetime import datetime


def add_anek(text, user=None):
    conn = sqlite3.connect('anek_base.db')
    cur = conn.cursor()
    timeformated = f'{datetime.now()}'
    cur.execute(f"""INSERT INTO anekdots(anektext, time) VALUES('{text}', '{timeformated}')""")
    conn.commit()
    conn.close()


def get_anek_random():
    conn = sqlite3.connect('anek_base.db')
    cur = conn.cursor()
    aneki = cur.execute(f"""SELECT anektext, time FROM anekdots""").fetchall()
    anek = random.choice(aneki)
    conn.close()
    return anek[0] + f'\n\nДобавлено {anek[1]}'


def get_named_anek(theme):
    conn = sqlite3.connect('anek_base.db')
    cur = conn.cursor()
    aneki = cur.execute(f"""SELECT anektext FROM anekdots""").fetchall()
    anek_chosen = [i[0] for i in aneki if theme.lower() in i[0].lower()]
    conn.close()
    return anek_chosen
