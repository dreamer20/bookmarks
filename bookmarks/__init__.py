from flask import Flask
from config import Config


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.from_mapping(test_config)

    from . import auth, index
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)

    from . import db
    db.init_app(app)

    return app
