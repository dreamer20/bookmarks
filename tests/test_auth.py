from bookmarks import db_api
import pytest


def test_register(app, client):
    response = client.post(
        '/auth/register',
        data={'login': 'new_user', 'password': 'password1234'}
    )

    assert response.status_code == 200
    with app.app_context():
        user = db_api.get_user_by_login('new_user')

        assert user is not None


@pytest.mark.parametrize(('login', 'password', 'message'), (
    ('a', '12345678', b'Login must be at least 3 characters, '),
    ('1romeo', '12345678', b'Login must be at least 3 characters, '),
    ('John', '123', b'Password must be at least 8 symbols.')
))
def test_register_validation(client, login, password, message):
    response = client.post(
        '/auth/register',
        data={'login': login, 'password': password}
    )

    assert message in response.data
