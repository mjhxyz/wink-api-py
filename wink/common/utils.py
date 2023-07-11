from datetime import datetime, date
from authlib.jose import jwt, JoseError

from flask.json.provider import DefaultJSONProvider, _default as _default_json
from flask import current_app

from wink.models.base import Base


def _default(o):
    if hasattr(o, 'to_dict'):
        d = o.to_dict()
        return o.to_dict()
    if isinstance(o, datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(o, date):
        return o.strftime('%Y-%m-%d')
    return _default_json(o)


class WinkJSONProvider(DefaultJSONProvider):
    default = staticmethod(_default)


def generate_token(payload: dict):
    header = {'alg': 'HS256'}
    key = current_app.config['SECRET_KEY']
    return jwt.encode(header=header, payload=payload, key=key).decode('utf-8')


def validate_token(token):
    key = current_app.config['SECRET_KEY']
    try:
        return jwt.decode(token, key)
    except JoseError:
        return False
