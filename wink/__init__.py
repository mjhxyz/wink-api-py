from flask import Flask

from wink.models.base import db


def register_blueprint(app):
    from wink.api.base import api
    app.register_blueprint(api)


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('wink.config.setting')
    app.config.from_object('wink.config.secure')

    register_blueprint(app)

    # 注册 SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
