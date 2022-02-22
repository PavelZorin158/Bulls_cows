from flask import Blueprint, url_for, request, redirect, flash

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/')
def index():
    print(url_for('.index'))
    return "adminka"

@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "admin":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title="Админ-панель")