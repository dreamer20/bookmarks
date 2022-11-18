import psycopg2 as pg2
import re
import functools
from .db_api import register_user, get_user_by_id, get_user_by_login
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, g, render_template, request, flash, redirect, url_for, session
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']
        error = None

        if len(password) < 8:
            error = 'Password must be at least 8 symbols.'

        if password != password2:
            error = "Passwords doesn't match."

        if re.match(r'^[a-zA-Z]\w{2,15}$', login) is None:
            error = (
                'Login must be at least 3 characters, '
                'starts from latin letter and length not more then 16 symbols'
            )

        if error is None:
            try:
                register_user(login, generate_password_hash(password))
            except pg2.IntegrityError:
                error = 'User with this login already exist.'
            except Exception:
                error = 'Error has occurred. Try again later.'
            else:
                redirect(url_for('auth.login'))

        if error:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        error = None
        user = get_user_by_login(login)

        if user is not None:
            if check_password_hash(user['hashed_password'], password):
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index.index'))
            else:
                error = 'Invalid login or password'
        else:
            error = 'Invalid login or password'

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
