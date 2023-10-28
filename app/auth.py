from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from functools import wraps

bp = Blueprint('a', __name__, url_prefix='/a')


def i(a):
    l = LoginManager()
    l.login_view = 'a.b'
    l.login_message = 'To access this page, you must go through an authentication procedure.'
    l.login_message_category = 'w'
    l.user_loader(m)
    l.init_app(a)


def m(i):
    u = User.query.get(i)
    return u


@bp.route('/b', methods=['GET', 'POST'])
def b():
    if request.method == 'POST':
        j = request.form.get('j')
        p = request.form.get('p')
        if j and p:
            u = User.query.filter_by(login=j).first()
            if u and u.check_password(p):
                login_user(u)
                flash('You have been successfully authenticated.', 's')
                n = request.args.get('n')
                return redirect(n or url_for('i'))
        flash('You have been successfully authenticated.', 'd')
    return render_template('a/l.html')


def p(a):
    def d(f):
        @wraps(f)
        def w(*args, **k):
            i = k.get('i')
            u = None
            if i:
                u = m(i)
            if not current_user.can(a, u):
                flash('Insufficient rights', 'w')
                return redirect(url_for('i'))
            return f(*args, **k)
        return w
    return d


@bp.route('/l')
@login_required
def l():
    logout_user()
    return redirect(url_for('i'))
