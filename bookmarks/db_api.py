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
    cursor.close()

    return user
