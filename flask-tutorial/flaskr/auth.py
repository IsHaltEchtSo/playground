import functools

from flask import \
    Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # receive username and password from the registration form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # validate if username and password are provided
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # register new user and commit to our database
        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # unless the user already exists
                error = f"User {username} is already registered."
            else:
                # EXIT 1: redirect to login when register was successful
                return redirect(url_for("auth.login"))
            
        flash(error)

    # EXIT 2: show a form to register
    return render_template('auth/register.html')


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # receive username and password from the request form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # query the user from the database
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # validate both username and password
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        # start a clean session and update the user_id
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # EXIT 1: redirect to the landing page
            return redirect(url_for('index'))

        flash(error)

    # EXIT 2: show a form to login
    return render_template('auth/login.html')


# this function is called prior to every request/view function
@bp.before_app_request
def load_logged_in_user():
    """Retrieve the user from the db if exists and store it in the session object"""
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
    return redirect(url_for('index'))


# decorator for views that require the client to be a logged-in user
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view