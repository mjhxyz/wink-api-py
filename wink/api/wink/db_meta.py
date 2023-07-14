from wink.api.base import api
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db

from sqlalchemy import inspect
from flask import current_app, request
from sqlalchemy.exc import NoSuchTableError
from flask_login import login_required


# 一定要鉴权
@api.get('/wink/db/table_list')
@login_required
def db_table_list():
    source = request.args.get('source', 'meta')
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
    return Success(data=table_names)


# 一定要鉴权
@api.get('/wink/db/source_list')
@login_required
def db_source_list():
    config = current_app.config
    result = ['meta']
    if 'DB_BI' in config:
        db_bi = config['DB_BI']
        result.extend(db_bi.keys())
    return Success(data=result)


# 一定要鉴权
@api.get('/wink/db/table_field_list')
@login_required
def table_field_list():
    table_name = request.args.get('table_name')
    source = request.args.get('source', 'meta')
    if source == 'meta':
        inspector = inspect(db.engine)
    else:
        config = current_app.config
        db_bi = config['DB_BI']
        if source not in db_bi:
            return NotFoundError('数据源不存在')
        inspector = inspect(db.get_engine(source))

    try:
        columns = inspector.get_columns(table_name)
    except NoSuchTableError:
        return NotFoundError('数据表不存在')
    result = []
    for column in columns:
        result.append({
            'name': column['name'],
            'type': str(column['type']),
            'nullable': column['nullable'],
            'default': column['default'],
            'comment': column['comment']
        })
    return Success(data=result)
