from bookmarks import db_api


def test_register_user(app):
    with app.app_context():
        db_api.register_user('login', 'hash_password')
        user = db_api.get_user_by_login('login')
        assert user['login'] == 'login'
