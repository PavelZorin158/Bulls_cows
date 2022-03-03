"""
введите "end" для завершения
"""
import os

from flask import Flask, render_template, url_for, request, flash, \
    session, redirect, abort, make_response
from random import randint
from cow_db import *
from admin.admin import admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghfgjhfghjghj'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

app.register_blueprint(admin, url_prefix='/admin')


def verifyExt(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == 'png' or ext == 'PNG':
        return True
    return False

@app.route("/")
def index():
    scores = score()
    if 'userLogged' in session:
        # если пользователь залогинен
        print(session['userLogged'])
        if avatar(session['userLogged']) == 'no_ava':
            # у текущего пользователя нет аватарки
            return render_template('index.html', scores=scores, username=session['userLogged'])
        else:
            # у текущего пользователя есть аватарка
            ava = 'yes'
            return render_template('index.html', scores=scores, username=session['userLogged'], ava=ava)
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


@app.route("/kolcif/<username>")
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


@app.route("/exit")
def exit():
    print(url_for('exit'))
    del session['userLogged']
    del session['th_num']
    del session['n']
    del session['popytka']
    del session['answers']
    del session['answern']
    return render_template('exit.html')


@app.route("/add_ava")
def add_ava():
    return render_template('add_ava.html', username=session['userLogged'])

@app.route("/userava")
def userava():
    img = avatar(session['userLogged'])
    if img == 'no_ava':
        print('читаем дефолтную')
        try:
            f = open(os.path.join('static\images', 'default.png'), 'rb')
            # Получаем бинарные данные нашего файла
            img = f.read()
            # Конвертируем данные
            # dat = sqlite3.Binary(img)
            f.close()
        except FileNotFoundError as e:
            print('не найден аватар по умолчанию: ' + str(e))
    h = make_response(img)
    #h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f: #and verifyExt(f.filename):
            # если файл передался и f существует и расширение PNG
            try:
                img = f.read()
                res = add_avatar(img, session['userLogged'])
                if res == 'ok':
                    flash("Аватар обновлен", "success")
                else:
                    flash("Ошибка обновления аватара", "error")
            except FileNotFoundError as e:
                print('Ошибка чтения файла'+str(e))
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")

    return redirect(url_for('add_ava'))

@app.route("/new", methods=["POST"])
def new():
    print(url_for('new'))
    # НАЧАЛО НОВОЙ ИГРЫ

    n = int(request.form['kol'])
    if n > 6:
        flash("Максимальное количество цифр 6", "error")
        scor = score(session['userLogged'])
        return render_template('kolcif.html', username=session['userLogged'], scor=scor)
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


@app.route("/appp", methods=["POST"])
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
    app.run(host="0.0.0.0", port=5000, debug=False)
    #app.run(host="192.168.0.110", port=5000, debug=False)
