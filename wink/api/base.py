from flask import Blueprint
from flask_login import LoginManager

login_manager = LoginManager()
api = Blueprint('api', __name__)
