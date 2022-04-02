import sqlite3 as sq


def start():
    global base, cur
    base = sq.connect('person.db')
    cur = base.cursor()
    if base:
        print("Database working!")
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, img_two TEXT)')
    base.commit()


async def add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?)', (data.get('Q1'), data.get('Q2'),))
        base.commit()


