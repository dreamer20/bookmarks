from .db_api import get_bookmarks
from .auth import login_required
from flask import (
    Blueprint, render_template, g
)

bp = Blueprint('index', __name__,)


@bp.route('/')
@login_required
def index():
    bookmarks = get_bookmarks(g.user['id'])
    return render_template('index.html', bookmarks=bookmarks)
