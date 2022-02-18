'''
Для localhost
введите "end" для завершения
'''

from flask import Flask, render_template, url_for, request, flash,\
    session, redirect, abort
from random import randint
from cow_db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghfgjhfghjghj'

answers = [] # список выданных ответов
answern = [] # список введенных цифр
th_num = '' # загадонное число
n = 0 # количество цифр
name = '' # текущее имя игрока
m = []
popytka = 0


@app.route("/") # используется
def index():
    print(url_for('index'))
    scores = score()
    return render_template('index.html', scores=scores)


@app.route("/login", methods=["POST", "GET"])
def login():
    global name

    if request.method == 'POST':
        nam = request.form['username']
        pas = request.form['psw']

    if 'userLogged' in session:
        # если userLogged приыутствует в session значит пользователь залогинен в этой
        # сессии и отправляем в profile имя пользователя из userLogged из session
        #session['userLogged'] = 'Rick'
        print('залогинен: '+session['userLogged'])
        name = session['userLogged']
        return redirect(url_for('kolcif', username=session['userLogged']))

    elif request.method == 'POST' and pas == pasword(nam):
        # если совпал пароль
        session['userLogged'] = nam
        name = nam
        print('входит: '+session['userLogged'])
        return redirect(url_for('kolcif', username=session['userLogged']))

    elif request.method == 'POST' and (request.form['username'] != '' or request.form['psw'] != ''):
        print('Не правельный логин или пороль')
        flash('Не правельный логин или пороль', category='error')

    return render_template('login.html', username='')


@app.route("/new_user", methods=["POST", "GET"])
def new_user():
    global name
    print(url_for('new_user'))
    if request.method == 'POST':
        nam = request.form['username']
        pas = request.form['psw']

        if pasword(nam) == 'no_user':
            # если в базе нет такого пользователя

            if pas == '':
                # если пустой пороль
                print('введен пустой пороль')
                flash('не введен пороль', category='error')
                return render_template('login.html', username='')
            else:
                # создаем нового игрока
                add_user(nam, pas)
                session['userLogged'] = nam
                name = nam
                print('создан пользователь: ' + session['userLogged'])
                return redirect(url_for('kolcif', username=session['userLogged']))

        else:
            # если такой пользователь уже есть
            print('такой пользователь уже есть')
            flash('такой пользователь уже существует', category='error')
            return render_template('login.html', username='')

    return render_template('login.html', username='')

@app.route("/unlogin")
def unlogin():
    print(url_for('unlogin'))
    del session['userLogged']
    return redirect(url_for('login'))

@app.route("/kolcif/<username>") # используется
def kolcif(username):
    scor = score(username)
    print(url_for('kolcif', username=session['userLogged']))
    if 'userLogged' not in session or session['userLogged'] != username:
        # проверяем, залогинен ли кто_то в сессии или вдруг кто_то умный
        # написал в строке адрес /profile/pavel
        print('фигня')
        abort(401)
    return render_template('kolcif.html', username=username, scor=scor)

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
    global name

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
        all_score = score(name)
        return render_template('win.html', ann =answern, ans=answers,
                               an=len(answers), num=str(popytka), win=th_num, scor=scor,
                               all_score=all_score)

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
    app.run(host="192.168.0.110",port=5000, debug=True)
