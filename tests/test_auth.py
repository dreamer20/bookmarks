from bookmarks import db_api
import pytest
from flask import session, g


def test_register(app, client):
    """ Register user """
    response = client.post(
        '/auth/register',
        data={'login': 'new_user', 'password': 'password1234', 'password2': 'password1234'}
    )

    assert response.status_code == 200
    with app.app_context():
        user = db_api.get_user_by_login('new_user')

        assert user is not None


@pytest.mark.parametrize(('login', 'password', 'password2', 'message'), (
    ('a', '12345678', '12345678', b'Login must be at least 3 characters, '),
    ('1romeo', '12345678', '12345678', b'Login must be at least 3 characters, '),
    ('John', '123', '123', b'Password must be at least 8 symbols.'),
    ('John', 'qwerqwer', 'qwerreqq', b'Passwords doesn&#39;t match.')
))
def test_register_validation(client, login, password, password2, message):
    """ Checks user input """
    response = client.post(
        '/auth/register',
        data={'login': login, 'password': password, 'password2': password2}
    )

    assert message in response.data


def test_login(client, auth):
    """ Login user to server """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.location == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['login'] == 'user1'
