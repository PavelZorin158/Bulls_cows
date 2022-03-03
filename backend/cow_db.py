''' Функции для работы с БД players '''

import sqlite3

def score(name = ''):
    # без параметра: возвращает список картежей с результатьми игроков [('str', int), ('Катя', 2100), ...]
    # c параметром (str) : возвращает счет игрока с именем str в виде числа int

    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()

        # удаляет таблицу players чтоб пересоздать ее
        # cur.execute("DROP TABLE IF EXISTS players")

        # создает таблицу players если ее нет
        cur.execute("""CREATE TABLE IF NOT EXISTS players(
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pas TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            avatar BLOB DEFAULT NULL
            )""")

        if name == '':
            cur.execute("SELECT name, score FROM players ORDER BY score DESC")
        else:
            cur.execute(f"SELECT score FROM players WHERE name = '{name}'")
            s = cur.fetchone()
            return s[0]
    return cur.fetchall()

def add_score(name, scor):
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        #cur.execute("SELECT * FROM players")
        cur.execute(f"UPDATE players SET score = score + {scor} WHERE name LIKE '{name}'")
        con.commit()
    return

def pasword(name):
    # возвращает 'no_user' если в базе нет name

    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT pas FROM players WHERE name = '{name}'")
        s = cur.fetchone()
        if s == None:
            # пользователь name не найден в базе
            return 'no_user'
        else:
            return s[0]

def avatar(name):
    # возвращает 'no_user' если в базе нет name
    # возвращает 'no_ava' усли у пользователя нет авы

    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT avatar FROM players WHERE name = '{name}'")
        s = cur.fetchone()
        if s == None:
            # пользователь name не найден в базе
            return 'no_user'
        elif s[0] is None:
            # у пользователя нету авы
            print('no ava')
            return 'no_ava'
        else:
            return s[0]



def add_avatar(img, name):
    # возвращает 'no_user' если в базе нет name
    if not img:
        print('в функцию add_avatar не пришло img')
        return 'no_img'
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT pas FROM players WHERE name = '{name}'")
        s = cur.fetchone()
        if s == None:
            # пользователь name не найден в базе
            return 'no_user'
        else:
            binary = sqlite3.Binary(img)
            cur.execute("UPDATE players SET avatar = ? WHERE name = ?", (binary, name))
            con.commit()
            return 'ok'


def add_user(name, pas):
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        #cur.execute(f"UPDATE players SET score = score + {scor} WHERE name LIKE '{name}'")
        new_user = (name, pas)
        cur.execute("INSERT INTO players(name, pas) VALUES(?, ?)", new_user)
        con.commit()
    return

def rename_user(name, newname):
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE players SET name = '{newname}' WHERE name LIKE '{name}'")
        con.commit()
    return

def repas_user(name, newpas):
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE players SET pas = '{newpas}' WHERE name LIKE '{name}'")
        con.commit()

    return
def rescor_user(name, newscore):
    with sqlite3.connect("../dir_db/cow.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE players SET score = {newscore} WHERE name LIKE '{name}'")
        con.commit()
    return