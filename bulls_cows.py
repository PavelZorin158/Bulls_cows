'''
Для localhost
введите "end" для завершения
'''

from flask import Flask, render_template, url_for, request, flash,\
    session, redirect, abort
from random import randint
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghfgjhfghjghj'

answers = [] # список выданных ответов
answern = [] # список введенных цифр
#keys = [{"name": "Новая игра", "url": "kolcif"},
#        {"name": "Выход", "url": "exit"}]
th_num = '' # загадонное число
n = 0 # количество цифр
name = 'Катя' # временное имя игрока
m = []
popytka = 0

def score():
    with sqlite3.connect("cow.db") as con:
        cur = con.cursor()
        # cur.execute("DROP TABLE IF EXISTS players") # чтоб пересоздать таблицу players
        cur.execute("""CREATE TABLE IF NOT EXISTS players(
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pas TEXT NOT NULL,
            score INTEGER DEFAULT 0
            )""")
        cur.execute("SELECT name, score FROM players")
    return cur.fetchall()

def add_score(name, scor):
    with sqlite3.connect("cow.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM players")
        for i in cur.fetchall():
            print(i)
        cur.execute(f"UPDATE players SET score = score + {scor} WHERE name LIKE '{name}'")
        con.commit()
    return


@app.route("/") # используется
def index():
    print(url_for('index'))
    scores = score()
    return render_template('index.html', scores=scores)


'''
@app.route("/profile/<username>")
def profile(username):
    print('username=', username)
    if 'userLogged' not in session or session['userLogged'] != username:
        # проверяем, залогинен ли кто_то в сессии или вдруг кто_то умный
        # написал в строке адрес /profile/pavel
        abort(401)
    return f"Профиль пользователя: {username}"
'''


@app.route("/login", methods=["POST", "GET"])
def login():
    #del session['userLogged']
    #print('/', session.keys())
    if 'userLogged' in session:
        # если userLogged приыутствует в session значит пользователь залогинен в этой
        # сессии и отправляем в profile имя пользователя из userLogged из session
        #session['userLogged'] = 'Rick'
        print('залогинен: '+session['userLogged'])
        return redirect(url_for('kolcif', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Rick' and request.form['psw'] == "123":
        # если совпал пароль
        session['userLogged'] = request.form['username']
        print('входит: '+session['userLogged'])
        return redirect(url_for('kolcif', username=session['userLogged']))
    elif request.method == 'POST' and (request.form['username'] != '' or request.form['psw'] != ''):
        print('Не правельный логин или пороль')
        flash('Не правельный логин или пороль', category='error')
    return render_template('login.html', username='')


@app.route("/unlogin")
def unlogin():
    print(url_for('unlogin'))
    del session['userLogged']
    return redirect(url_for('login'))

@app.route("/kolcif/<username>") # используется
def kolcif(username):
    print(url_for('kolcif', username=session['userLogged']))
    if 'userLogged' not in session or session['userLogged'] != username:
        # проверяем, залогинен ли кто_то в сессии или вдруг кто_то умный
        # написал в строке адрес /profile/pavel
        print('фигня')
        abort(401)
    return render_template('kolcif.html', username=username)

@app.route("/game")
def game():
    print(url_for('game'))
    return render_template('game.html', ann=answern, ans=answers,
                           an=len(answers), num=str(popytka), win='NO')

@app.route("/exit") # используется
def exit():
    print(url_for('exit'))
    return render_template('exit.html')


@app.route("/new", methods=["POST"]) # используется
def new():
    print(url_for('new'))
    # НАЧАЛО НОВОЙ ИГРЫ
    # загадонное число
    global th_num
    global answers
    global m
    global n
    global popytka
    n = int(request.form['kol'])
    zz = str(randint(0, 10 ** n - 1))
    th_num = ('0' * (n - len(zz))) + zz
    print('загадано', th_num)
    answers.clear()
    m = [j for j in th_num]
    popytka = 1
    return render_template('game.html', ann=answern, ans=answers,
                           an=len(answers), num=str(popytka))


@app.route("/appp", methods=["POST"]) # используется
def appp():
    global th_num
    global answers
    global answern
    global m
    global n
    global popytka
    print(url_for('appp'))
    number = str(request.form['number'])
    print(number, th_num)
    if (number == 'end') or (number == 'END'):
        # Выход
        scores = score()
        return render_template('index.html', scores=scores)
    if not number.isdecimal():
        # если введены не цифры
        flash('Пишите только цифры', category='error')
        return render_template('game.html', ann=answern, ans=answers,
                               an=len(answers), num=str(popytka), win='NO', val='вводите только цифры')
    if len(number) != n:
        # если введено не правильное количество цифр
        flash('вводите '+str(n)+' цифры', category='error')
        return render_template('game.html', ann=answern, ans=answers,
                               an=len(answers), num=str(popytka), win='NO', val='вводите '+str(n)+' цифры')
    a = [j for j in number]
    m = [j for j in th_num]
    popytka += 1
    if number == th_num:
        # ПОБЕДА
        scor = 1
        popytka -= 1
        for i in range(n):
            scor = scor * 10
        max_popyt = n * 10
        scor = scor * (max_popyt - popytka + 1)
        print('победа '+str(scor)+' очков')
        add_score(name, scor)
        return render_template('win.html', ann =answern, ans=answers,
                               an=len(answers), num=str(popytka), win=th_num, scor=scor)
    # проверяем на быков
    for i in range(n):
        if a[i] == th_num[i]:
            m[i] = 'b'
            a[i] = 'B'
    # проверяем на коров
    for i in range(n):
        if m.count(a[i]) > 0:
            found = m.index(a[i])
            m[found] = 'k'
    bulls = m.count('b')
    cows = m.count('k')
    answers.append(' - '+str(bulls)+' быков  '+str(cows)+' коров')
    answern.append(number)
    print(bulls, 'БЫКОВ  ', cows, 'КОРОВ')
    return render_template('game.html', ann=answern, ans=answers,
                           an=len(answers), num=str(popytka), win='NO')


@app.route("/win")
def win():
    print(url_for('win'))
    return render_template('win.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000, debug=True)
