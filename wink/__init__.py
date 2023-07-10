from flask import Flask
from werkzeug.exceptions import HTTPException

from wink.models.base import db
from wink.common.utils import WinkJSONProvider


def register_blueprint(app: Flask):
    from wink.api.base import api
    app.register_blueprint(api)


def register_error_handler(app: Flask):

    @app.errorhandler(Exception)
    def framework_error(e):
        from wink.common.error import APIException
        from wink.common.resp import ServerError, NotFoundError

        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 3000
            if code == 404:
                return NotFoundError()
            return APIException(error_code, msg, None)

        # 未知错误
        if app.config['DEBUG']:
            # TODO 记录日志
            raise e
        return ServerError()


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('wink.config.setting')
    app.config.from_object('wink.config.secure')

    register_blueprint(app)

    # 注册 SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_error_handler(app)

    app.json = WinkJSONProvider(app)

    return app
