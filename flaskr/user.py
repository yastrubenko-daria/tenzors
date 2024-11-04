import functools # декоратор
from flask import flash,  Blueprint, g, redirect, request, session, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flaskr.db import get_db
from http import HTTPStatus


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =="POST":
        userlogin = request.form['userlogin']
        username = request.form['username']
        surname = request.form['surname']
        age = request.form['age']
        password = request.form['password']

        db = get_db()
        error = None
        if not userlogin:
            error = 'Userlogin is required.'
        if not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (userlogin, username, surname, age, password) VALUES (?, ?, ?, ?, ?)",
                    (userlogin, username, surname, age,  generate_password_hash(password)), #кодировка паролей
                )
                db.commit()
            except db.IntegrityError:
                error = f"Userlogin {userlogin} is already registered."
            else:
                return redirect(url_for("user.login")) # отправление к входу
        flash(error)
    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=="POST":
        userlogin = request.form['userlogin']
        password = request.form['password']
        db = get_db()
        user = db.execute(
        'SELECT * FROM user WHERE userlogin = ?', (userlogin,)
        ).fetchone()
        error=None
        if user is None:
            error=HTTPStatus.UNAUTHORIZED
        if not check_password_hash(user['password'], password):
            error=HTTPStatus.UNAUTHORIZED
        if error is None:
            session.clear() # данные между запросами
            session['user_id'] = user['id']
            return redirect(url_for('user.account', user_id=user['id']))
        flash(error)
    return render_template('user/login.html')

def get_user(id):
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?',(id,)
    ).fetchone()
    if user is None:
        abort(404, f"User id {id} doesn't exist.")
    return user

@bp.route('/account/<int:user_id>', methods=["GET", "POST"])
def account(user_id):
    user = get_user(user_id)
    return render_template('user/account.html', user=user, user_id=user['id'])

@bp.route('/account/<int:user_id>/edit', methods=["GET", "POST"])
def edit_account(user_id):
    user=get_user(user_id)
    if request.method == 'POST':
        userlogin = request.form['userlogin']
        username = request.form['username']
        surname = request.form['surname']
        age = request.form['age']
        error = None
        if not userlogin:
            error = 'Userlogin is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE user SET userlogin = ?, username = ?, surname = ?, age = ?'
                ' WHERE id = ?',
                (userlogin, username, surname, age, user_id))
            db.commit()
            return redirect(url_for("user.account", user_id=user['id']))  # отправление к входу
    return render_template('user/edit.html', user=user, user_id=user['id'])

@bp.get('/account/<int:user_id>/deleted')
def deleted(user_id):
    user=get_user(user_id)
    login=user['userlogin']
    db=get_db()
    db.execute('DELETE FROM user WHERE id = ?', (user_id,))
    db.commit()
    return render_template('user/delete.html', login=login, user_id=user['id'])


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.index'))

#создание декоратора
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

 #todo: get user lk

