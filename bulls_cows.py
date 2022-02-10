# введите "end" для завершения
from flask import Flask, render_template, url_for, request, flash
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghfgjhfghjghj'

answers = [] # список выданных ответов
answern = [] # список введенных цифр
keys = [{"name": "Новая игра", "url": "kolcif"},
        {"name": "Выход", "url": "exit"}]
th_num = '' # загадонное число
n = 0 # количество цифр
m = []
popytka = 0

@app.route("/kolcif")
def kolcif():
    print(url_for('kolcif'))
    return render_template('kolcif.html')

@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', keys=keys)

@app.route("/game")
def game():
    print(url_for('game'))
    return render_template('game.html', ann=answern, ans=answers,
                           an=len(answers), num=str(popytka), win='NO')


@app.route("/exit")
def exit():
    print(url_for('exit'))
    return render_template('exit.html')


@app.route("/win")
def win():
    print(url_for('win'))
    return render_template('win.html')


@app.route("/appp", methods=["POST"])
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
        return render_template('index.html', keys=keys)
    if not number.isdecimal():
        flash('Пишите только цифры', category='error')
        return render_template('game.html', ann=answern, ans=answers,
                               an=len(answers), num=str(popytka), win='NO', val='вводите только цифры')
    if len(number) != n:
        flash('вводите '+str(n)+' цифры', category='error')
        return render_template('game.html', ann=answern, ans=answers,
                               an=len(answers), num=str(popytka), win='NO', val='вводите '+str(n)+' цифры')
    a = [j for j in number]
    m = [j for j in th_num]
    popytka += 1
    if number == th_num:
        # ПОБЕДА
        return render_template('win.html', ann =answern, ans=answers,
                               an=len(answers), num=str(popytka), win=th_num)

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


@app.route("/new", methods=["POST"])
def new():
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


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000, debug=False)
