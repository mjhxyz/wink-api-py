from flask import Flask


def register_blueprint(app):
    from wink.api.base import api
    app.register_blueprint(api)


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('wink.config.setting')
    app.config.from_object('wink.config.secure')

    register_blueprint(app)
    return app
