import os

from flask import Flask

from .db import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB_PATH = os.path.join(app.instance_path, 'detector.sqlite3')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=DB_PATH,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_PATH}'
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import images
    app.register_blueprint(images.bp)
    app.add_url_rule('/', endpoint='images')

    return app
