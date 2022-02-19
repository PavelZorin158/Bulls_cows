"""
введите "end" для завершения
"""

from flask import Flask, render_template, url_for, request, flash, \
    session, redirect, abort
from random import randint
from cow_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghfgjhfghjghj'


@app.route("/")  # используется
def index():
    print(url_for('index'))
    scores = score()
    return render_template('index.html', scores=scores)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        # если userLogged приыутствует в session значит пользователь залогинен в этой
        # сессии и отправляем в kolcif имя пользователя из userLogged из session
        print('уже залогинен: ' + session['userLogged'])
        return redirect(url_for('kolcif', username=session['userLogged']))

    if request.method == 'POST':
        nam = request.form['username']
        pas = request.form['psw']
        if pas == pasword(nam):
            # если совпал пароль
            session['userLogged'] = nam  # текущее имя игрока
            session['th_num'] = ''  # загадонное число
            session['n'] = 0  # количество цифр в загаданном числе
            session['popytka'] = 0  # количество попыток
            answers = []  # список выданных ответов
            session['answers'] = answers
            answern = []  # список введенных цифр
            session['answern'] = answern
            print('входит: ' + session['userLogged'])
            return redirect(url_for('kolcif', username=session['userLogged']))

        if request.form['username'] != '' or request.form['psw'] != '':
            print('Не правельный логин или пороль')
            flash('Не правельный логин или пороль', category='error')
    return render_template('login.html', username='')


@app.route("/new_user", methods=["POST", "GET"])
def new_user():
    print(url_for('new_user'))
    if request.method == 'POST':
        nam = request.form['username']
        pas = request.form['psw']

        if nam != '' and pasword(nam) == 'no_user':
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
                session['th_num'] = ''
                session['n'] = 0
                session['popytka'] = 0
                session['answers'] = []
                session['answern'] = []
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
    del session['th_num']
    del session['n']
    del session['popytka']
    del session['answers']
    del session['answern']
    return redirect(url_for('login'))


@app.route("/kolcif/<username>")  # используется
def kolcif(username):
    # хороший вопрос, если все данные брать из session, зачем тогда вообще
    # передавать username? так сложилось потом подумаю :)
    scor = score(session['userLogged'])
    print(url_for('kolcif', username=session['userLogged']))
    if 'userLogged' not in session or session['userLogged'] != username:
        # проверяем, залогинен ли кто_то в сессии или вдруг кто_то умный
        # написал в строке адрес /profile/pavel
        print('фигня')
        abort(401)
    return render_template('kolcif.html', username=session['userLogged'], scor=scor)


# @app.route("/game")
# def game():
#    print(url_for('game'))
#    return render_template('game.html', ann=answern, ans=answers,
#                           an=len(answers), num=str(popytka), win='NO')

@app.route("/exit")  # используется
def exit():
    print(url_for('exit'))
    del session['userLogged']
    del session['th_num']
    del session['n']
    del session['popytka']
    del session['answers']
    del session['answern']
    return render_template('exit.html')


@app.route("/new", methods=["POST"])  # используется
def new():
    print(url_for('new'))
    # НАЧАЛО НОВОЙ ИГРЫ

    n = int(request.form['kol'])
    session['n'] = n
    zz = str(randint(0, 10 ** n - 1))
    th_num = ('0' * (n - len(zz))) + zz
    session['th_num'] = th_num
    print('загадано', th_num)
    answers = []
    session['answers'] = []
    answern = []
    session['answern'] = []
    # m = [j for j in th_num]
    popytka = 1
    session['popytka'] = 1
    return render_template('game.html', ann=answern, ans=answers,
                           an=len(answers), num=str(popytka))


@app.route("/appp", methods=["POST"])  # используется
def appp():
    print(url_for('appp'))
    number = str(request.form['number'])
    print(number, session['th_num'])
    if (number == 'end') or (number == 'END'):
        # Выход
        scores = score()
        return render_template('index.html', scores=scores)
    if not number.isdecimal():
        # если введены не цифры
        flash('Пишите только цифры', category='error')
        return render_template('game.html', ann=session['answern'], ans=session['answers'],
                               an=len(session['answers']), num=str(session['popytka']), win='NO')
    if len(number) != session['n']:
        # если введено не правильное количество цифр
        flash('вводите ' + str(session['n']) + ' цифры', category='error')
        return render_template('game.html', ann=session['answern'], ans=session['answers'],
                               an=len(session['answers']), num=str(session['popytka']), win='NO')
    a = [j for j in number]
    m = [j for j in session['th_num']]

    if number == session['th_num']:
        # ПОБЕДА
        scor = 1
        for i in range(session['n']):
            scor = scor * 10
        max_popyt = session['n'] * 10
        scor = scor * (max_popyt - session['popytka'] + 1)
        print('победа ' + str(scor) + ' очков')
        add_score(session['userLogged'], scor)
        all_score = score(session['userLogged'])
        return render_template('win.html', ann=session['answern'], ans=session['answers'],
                               an=len(session['answers']), num=str(session['popytka']),
                               win=session['th_num'], scor=scor,
                               all_score=all_score)
    session['popytka'] += 1

    # проверяем на быков
    th_num = session['th_num']
    for i in range(session['n']):
        if a[i] == th_num[i]:
            m[i] = 'b'
            a[i] = 'B'
    # проверяем на коров
    for i in range(session['n']):
        if m.count(a[i]) > 0:
            found = m.index(a[i])
            m[found] = 'k'
    bulls = m.count('b')
    cows = m.count('k')
    session['answers'].append(' - ' + str(bulls) + ' быков  ' + str(cows) + ' коров')
    session['answern'].append(number)
    print(bulls, 'БЫКОВ  ', cows, 'КОРОВ')
    return render_template('game.html', ann=session['answern'], ans=session['answers'],
                           an=len(session['answers']), num=str(session['popytka']), win='NO')


@app.route("/win")
def win():
    print(url_for('win'))
    return render_template('win.html')


if __name__ == "__main__":
    app.run(host="192.168.0.110", port=5000, debug=False)
