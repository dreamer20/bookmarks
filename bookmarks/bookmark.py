import psycopg2 as pg2
import re
from .db_api import add_bookmark
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
            try:
                add_bookmark(url, g.user['id'])
            except pg2.IntegrityError:
                flash("Url adress isn't valid.")
            except Exception:
                flash('Error has occurred. Try again later.')
            else:
                return redirect(url_for('index.index'))

    return render_template('bookmark.html')
