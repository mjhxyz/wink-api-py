from datetime import datetime, date

from flask.json.provider import DefaultJSONProvider, _default as _default_json

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
