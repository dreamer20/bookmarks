from .db import get_db
import psycopg2.extras as extras


def register_user(login, hash_password):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'INSERT INTO users (login, hashed_password) VALUES (%s, %s)',
        (login, hash_password)
    )
    cursor.close()
    db.commit()


def get_random_user():
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'SELECT * FROM users'
    )
    user = cursor.fetchone()

    return user


def get_user_by_login(login):
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'SELECT * FROM users WHERE login = %s',
        (login, )
    )
    user = cursor.fetchone()
    cursor.close()

    return user


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'SELECT * FROM users WHERE id = %s',
        (user_id, )
    )
    user = cursor.fetchone()

    return user


def add_bookmark(url, title, icon_url, user_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'INSERT INTO bookmarks (url, title, icon_url, owner_id) \
         VALUES (%s, %s, %s, %s) RETURNING *',
        (url, title, icon_url, user_id, )
    )
    bookmark = cursor.fetchone()

    cursor.close()
    db.commit()

    return bookmark


def get_bookmarks(user_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'SELECT * FROM bookmarks WHERE owner_id = %s',
        (user_id, )
    )
    bookmarks = cursor.fetchall()

    cursor.close()
    db.commit()

    return bookmarks


def get_bookmark_by_id(bookmark_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=extras.DictCursor)

    cursor.execute(
        'SELECT * FROM bookmarks WHERE id = %s',
        (bookmark_id, )
    )
    bookmark = cursor.fetchone()

    cursor.close()
    db.commit()

    return bookmark


def delete_bookmark(bookmark_id, user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'DELETE FROM bookmarks WHERE id = %s AND owner_id = %s',
        (bookmark_id, user_id, )
    )

    cursor.close()
    db.commit()
