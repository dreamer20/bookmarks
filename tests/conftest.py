import pytest
from bookmarks import create_app
from bookmarks.db import init_db


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
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
