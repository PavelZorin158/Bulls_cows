from flask import Blueprint, url_for, request, redirect, flash, session, render_template, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'}]

db = None
@admin.before_request
def befor_request():
    # Установление соединения с БД перед выполнением запроса
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request

@admin.route('/')
def index():
    print(url_for('.index'))
    if 'admin_logged' not in session:
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')

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


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    # выходит из профиля админа
    print(url_for('.logout'))
    if 'admin_logged' in session:
        session.pop('admin_logged', None)
    return redirect(url_for('.login'))