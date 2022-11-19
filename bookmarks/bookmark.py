import psycopg2 as pg2
import re
import html
import requests
from .db_api import add_bookmark, delete_bookmark
from .auth import login_required
from flask import (
    Blueprint, g, render_template, request, flash, redirect, url_for
)


bp = Blueprint('bookmark', __name__, url_prefix='/bookmark')


@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    if request.method == 'POST':
        url = request.form['url']
        if re.match(r'^http(s?)://', url) is None:
            flash("Url adress isn't valid.")
        else:
            icon_url = get_website_icon_url(url)
            title = get_website_title(url)

            try:
                add_bookmark(url, title, icon_url, g.user['id'])
            except pg2.IntegrityError:
                flash("Url adress isn't valid.")
            except Exception:
                flash('Error has occurred. Try again later.')
            else:
                return redirect(url_for('index.index'))

    return render_template('bookmark.html')


def get_website_icon_url(url):
    match = re.match(r'^http(s?)://(.+?)([^/]+)', url)
    root = match.group(0)

    return root + '/favicon.ico'


def get_website_title(url):
    response = requests.get(url)
    match = re.search(r'<title>.+</title>', response.text)

    if match:
        title = match.group(0)[7:-8]
    else:
        title = 'Bookmark Title'

    return html.unescape(title)


@bp.route('/delete/<bookmark_id>', methods=['GET'])
@login_required
def delete(bookmark_id):
    try:
        delete_bookmark(bookmark_id, g.user['id'])
    except Exception:
        flash('Error has occurred. Try again later.')

    return redirect(url_for('index.index'))
