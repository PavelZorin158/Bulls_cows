import os
import sqlite3

try:
    f = open(os.path.join('static\images', '2.jpg'), 'rb')
    # Получаем бинарные данные нашего файла
    img = f.read()
    # Конвертируем данные
    #dat = sqlite3.Binary(img)
    f.close()

    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS images(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                avatar BLOB)""")
    #cur.execute("INSERT INTO Images(avatar) VALUES (?)", (dat,))
    id = 1
    cur.execute("UPDATE Images SET avatar = ? WHERE id = ?", (img, id))
    con.commit()

    cur.execute("SELECT avatar FROM Images WHERE id = 2")
    s = cur.fetchone() # возвращает картеж
    img = s[0]
    f = open(os.path.join('static\images', '_2_.jpg'), 'wb')
    f.write(img)
    f.close()
finally:
    if con:
        # Закрываем подключение с базой данных
        con.close()

    # data = readImage('1.jpg')
    # binary = sqlite3.Binary(data)

    # Готовим запрос в базу
    # cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,))
    # cur.execute(f"UPDATE players SET avatar = {binary} WHERE name LIKE 'Павел'")
    # cur.execute(f"UPDATE players SET score = 1 WHERE name LIKE '{name}'")

    # Выполняем запрос

# В случаи ошибки выводим ее текст.
