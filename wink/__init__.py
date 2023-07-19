from flask import Flask
from werkzeug.exceptions import HTTPException

from wink.models.base import db
from wink.common.utils import WinkJSONProvider


def register_blueprint(app: Flask):
    from wink.api.base import api
    app.register_blueprint(api)


def pre_process_config(app: Flask):
    config = app.config
    if 'DB_META' not in config:
        raise Exception('请先配置 DB_META 参数!!!')
    config['SQLALCHEMY_DATABASE_URI'] = config['DB_META']
    if 'DB_BI' in config:
        db_bi = config['DB_BI']
        if 'meta' in db_bi:
            raise Exception('DB_BI 中不能包含 meta 数据源!!!')
        config['SQLALCHEMY_BINDS'] = config['DB_BI']


def register_plugin(app: Flask):

    # Custom JSON provider
    app.json = WinkJSONProvider(app)
    # Flask-Login
    from wink.api.base import login_manager
    login_manager.init_app(app)
    # SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()


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

    # import flask_login
    # flask_login.login_required = lambda f: f

    pre_process_config(app)

    register_blueprint(app)
    register_error_handler(app)
    register_plugin(app)

    return app
