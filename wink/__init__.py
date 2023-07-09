from flask import Flask


def register_blueprint(app):
    pass


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('wink.config.secure')
    app.config.from_object('wink.config.setting')

    register_blueprint(app)
    return app
