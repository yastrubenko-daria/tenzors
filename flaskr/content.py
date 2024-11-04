import functools
from flask import flash,  Blueprint, g, redirect, request, session, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from http import HTTPStatus


bp = Blueprint('content', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    return render_template('index.html')