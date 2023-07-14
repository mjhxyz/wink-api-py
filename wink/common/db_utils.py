from wink.models.base import db
from wink.common.resp import NotFoundError

from sqlalchemy import inspect
from flask import current_app
from sqlalchemy.exc import NoSuchTableError


def get_source_list():
    config = current_app.config
    result = ['meta']
    if 'DB_BI' in config:
        db_bi = config['DB_BI']
        result.extend(db_bi.keys())
    return result


def get_table_list(source):
    table_names = []
    if source == 'meta':
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
    else:
        config = current_app.config
        db_bi = config['DB_BI']
        if source not in db_bi:
            return NotFoundError('数据源不存在')
        inspector = inspect(db.get_engine(source))
        table_names = inspector.get_table_names()
    return table_names


def get_table_field_list(source, table_name):
    if source == 'meta':
        inspector = inspect(db.engine)
    else:
        config = current_app.config
        db_bi = config['DB_BI']
        if source not in db_bi:
            raise NotFoundError('数据源不存在')
        inspector = inspect(db.get_engine(source))

    try:
        columns = inspector.get_columns(table_name)
    except NoSuchTableError:
        raise NotFoundError('数据表不存在')
    result = []
    for column in columns:
        result.append({
            'name': column['name'],
            'type': str(column['type']),
            'nullable': column['nullable'],
            'default': column['default'],
            'comment': column['comment']
        })
    return result
