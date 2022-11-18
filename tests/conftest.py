import os
import pytest
from bookmarks import create_app
from bookmarks.db import init_db, get_db


with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': 'postgres',
        'DATABASE_USER': 'postgres',
        'DATABASE_PASSWORD': 'peri54ri7end',
        'DATABASE_HOST': 'localhost'
    })

    with app.app_context():
        init_db()
        db = get_db()
        cursor = db.cursor()
        cursor.execute(_data_sql)
        cursor.close()
        db.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, login='user1', password='12345678'):
        return self._client.post(
            '/auth/login',
            data={'login': login, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
