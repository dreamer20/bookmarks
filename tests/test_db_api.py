from bookmarks import db_api


def test_register_user(app):
    with app.app_context():
        db_api.register_user('login', 'hash_password')
        user = db_api.get_user_by_login('login')

        assert user['login'] == 'login'


def test_add_bookmark(app):
    with app.app_context():
        user = db_api.get_user_by_login('user1')
        bookmark = db_api.add_bookmark('http://test.com', user['id'])

        assert bookmark['url'] == 'http://test.com'


def test_get_bookmarks(app):
    with app.app_context():
        user = db_api.get_user_by_login('user1')
        db_api.add_bookmark('http://test.com', user['id'])
        db_api.add_bookmark('http://testtest.com', user['id'])
        bookmarks = db_api.get_bookmarks(user['id'])

        assert isinstance(bookmarks, list)
        assert len(bookmarks) == 2
