from wink.models.base import db
from wink.common.resp import NotFoundError

from sqlalchemy import inspect, MetaData, Table
from flask import current_app
from sqlalchemy.exc import NoSuchTableError


def get_source_engine(source):
    config = current_app.config
    if source == 'meta':
        return db.engine
    if not is_source_exists(source):
        raise NotFoundError('数据源不存在')
    db_bi = config['DB_BI']
    return db.get_engine(source)


def execute_sql(source, sql):
    engine = get_source_engine(source)
    with engine.connect() as conn:
        res = conn.execute(sql)
        mapping_list = res.mappings().all()
        result = []
        for mapping in mapping_list:
            result.append(dict(mapping))
        return result


def generate_table(source, table_name):
    engine = get_source_engine(source)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return Table(table_name, metadata, autoload=True)


def is_source_exists(source):
    config = current_app.config
    if source == 'meta':
        return True
    if 'DB_BI' not in config:
        return False
    db_bi = config['DB_BI']
    return source in db_bi


def get_source_inspector(source):
    config = current_app.config
    if source == 'meta':
        return inspect(db.engine)
    if not is_source_exists(source):
        raise NotFoundError('数据源不存在')
    return inspect(db.get_engine(source))


def get_source_list():
    config = current_app.config
    result = ['meta']
    if 'DB_BI' in config:
        db_bi = config['DB_BI']
        result.extend(db_bi.keys())
    return result


def get_table_list(source):
    table_names = []
    inspector = get_source_inspector(source)
    table_names = inspector.get_table_names()
    return table_names


def get_table_field_list(source, table_name):
    inspector = get_source_inspector(source)
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


def get_primary_key(source, table_name):
    inspector = get_source_inspector(source)
    try:
        primary_key = inspector.get_pk_constraint(
            table_name)['constrained_columns']
        return primary_key
    except NoSuchTableError:
        raise NotFoundError('数据表不存在')
