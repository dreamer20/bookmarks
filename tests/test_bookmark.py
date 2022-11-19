from flask import g
import pytest
from bookmarks.db_api import get_bookmark_by_id
from bookmarks.bookmark import get_website_title, get_website_icon_url


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


def test_get_website_title():
    title = get_website_title('https://requests.readthedocs.io/en/latest/user/quickstart/#response-content')
    assert title == 'Quickstart — Requests 2.28.1 documentation'


@pytest.mark.parametrize('url, result', (
    ('https://docs.python.org/3/reference/lexical_analysis.html?highlight=comments', 'https://docs.python.org/favicon.ico'),
    ('http://docs.python.org/3/reference/lexical_analysis.html?highlight=comments', 'http://docs.python.org/favicon.ico'),
    ('https://stackoverflow.com/questions/32082285/using', 'https://stackoverflow.com/favicon.ico'),
    ('https://console.clever-cloud.com/', 'https://console.clever-cloud.com/favicon.ico'),
    ('https://getbootstrap.com', 'https://getbootstrap.com/favicon.ico')))
def test_get_website_icon_url(url, result):
    icon_url = get_website_icon_url(url)

    assert icon_url == result


def test_delete_bookmark(client, auth, app):
    """ Should delete bookmark from database """
    bookmark_id = 1
    auth.login(login='user2', password='123456789')
    with client:
        client.get('/')
        response = client.get(
            '/bookmark/delete/1',
            follow_redirects=True
        )

        response.location == '/'

    with app.app_context():
        assert get_bookmark_by_id(bookmark_id) is None
