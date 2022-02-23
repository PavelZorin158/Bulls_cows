from flask import Blueprint, url_for, request, redirect, flash, session, render_template
from cow_db import *

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'}]


@admin.route('/')
def index():
    print(url_for('.index'))
    if 'admin_logged' not in session:
        return redirect(url_for('.login'))
    scores = score()
    return render_template('admin/index.html', menu=menu, scores=scores, title='Админ-панель')

@admin.route('/login', methods=["POST", "GET"])
def login():
    print(url_for('.login'))
    if 'admin_logged' in session:
        print('админ залогинен в сессии')
        return redirect(url_for('.index'))
    if request.method == "POST":
        print('имя: '+str(request.form['user'])+'   пороль: '+str(request.form['psw']))
        # если пороль админа совпал
        if request.form['user'] == "admin" and request.form['psw'] == "admin":
            print('OK')
            session['admin_logged'] = 1
            return redirect(url_for('.index'))
        else:
            print('acses denid')
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title="Админ-панель")


@admin.route('/logout')
def logout():
    # выходит из профиля админа
    print(url_for('.logout'))
    if 'admin_logged' in session:
        session.pop('admin_logged', None)
        if 'userLogged' in session:
            del session['userLogged']
    return redirect(url_for('index'))

@admin.route("/edit/<user>", methods=["POST", "GET"])
def edit(user):
    print(user)
    if 'admin_logged' not in session:
        return redirect(url_for('.login'))
    if request.method == "POST":
        repas_user(user, request.form['psw'])
        rescor_user(user, int(request.form['scor']))
        rename_user(user, request.form['name'])
        user = request.form['name']
        flash("Данные пользователя обновлены", "success")
        return redirect(user)
    session['userLogged'] = user
    score_user = score(user)
    psw_user = pasword(user)
    return render_template('admin/edit.html', menu=menu, user=user, score=score_user, pasword=psw_user )

@admin.route('/admin_upload', methods=["POST", "GET"])
def admin_upload():
    if request.method == 'POST':
        f = request.files['file']
        if f: #and verifyExt(f.filename):
            # если файл передался и f существует и расширение PNG
            try:
                img = f.read()
                res = add_avatar(img, session['userLogged'])
                if res == 'ok':
                    flash("Аватар обновлен", "success")
                    print('аватар обновлен админом')
                else:
                    flash("Ошибка обновления аватара", "error")
            except FileNotFoundError as e:
                print('Ошибка чтения файла'+str(e))
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")

    return render_template('admin/edit.html', menu=menu, user=session['userLogged'])
