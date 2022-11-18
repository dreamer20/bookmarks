from flask import g
import pytest


def test_add_bookmark_unauthorized(client):
    """ Sends user to login page if he tries add bookmark unauthorized """
    response = client.post(
        '/bookmark/add',
        data={'url': 'http://some.com', 'owner_id': 1}
    )

    assert response.location == '/auth/login'


@pytest.mark.parametrize('url, message', (
    ('', b'Url adress isn&#39;t valid.'),
    (' ', b'Url adress isn&#39;t valid.'),
    ('12345', b'Url adress isn&#39;t valid.')
))
def test_add_bookmark_validation(client, url, message, auth):
    """ Checks if user input is valid """
    auth.login()
    with client:
        client.get('/')
        response = client.post(
            '/bookmark/add',
            data={'url': url, 'owner_id': g.user['id']}
        )

    assert message in response.data


def test_add_bookmark(client, auth):
    """ Adds bookmark to the database """
    auth.login()
    with client:
        client.get('/')
        response = client.post(
            '/bookmark/add',
            data={'url': 'http://some.com', 'owner_id': g.user['id']},
            follow_redirects=True
        )

    # assert response.location == '/'
    assert b'http://some.com' in response.data


def test_get_all_bookmarks(client, auth):
    """ Gets all user bookmarks on the front page """
    auth.login(login='user2', password='123456789')
    with client:
        response = client.get('/')

    assert b'https://test.com' in response.data
    assert b'https://test2.com' in response.data
    assert b'https://test3.com' in response.data
