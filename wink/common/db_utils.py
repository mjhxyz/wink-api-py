from wink.models.base import db
from wink.common.resp import NotFoundError

from sqlalchemy import inspect, MetaData, Table
from flask import current_app
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import Integer, String, Text, Float, Date, DateTime, Boolean, JSON, LargeBinary, Numeric
from sqlalchemy.dialects.mysql import TINYINT


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
            'type_obj': column['type'],  # 真实类型
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


###################### 字段处理 Start ######################
def parse_comment(comment):
    # 解析 comment
    # 字段名: 1=正常, 2=异常, 3=未知
    # 返回: 字段名, {1: '正常', 2: '异常', 3: '未知'}
    # 返回: comment, {}
    normal = comment, None
    if not isinstance(comment, str) or ':' not in comment:
        return normal
    comment_list = comment.split(':')
    if len(comment_list) != 2:
        return normal
    field_name = comment_list[0].strip()
    vals = comment_list[1].strip()
    if not vals or not field_name:
        return normal
    val_list = vals.split(',')
    result = {}
    for val in val_list:
        val_list = val.split('=')
        if len(val_list) != 2:
            return normal
        result[val_list[0].strip()] = val_list[1].strip()
    return field_name, result


def get_field_compo(field):
    # 获取字段所用组件
    type_obj = field['type_obj']
    sqlalchemy_type = type_obj.type

    if isinstance(sqlalchemy_type, String):
        return '文本框'
    if isinstance(sqlalchemy_type, Text):
        return '文本域'
    if isinstance(sqlalchemy_type, Integer):
        return '整数框'
    if isinstance(sqlalchemy_type, Float):
        return '浮点框'
    if isinstance(sqlalchemy_type, Date):
        return '日期框'
    if isinstance(sqlalchemy_type, DateTime):
        return '日期时间框'

    field_label, field_mappping = db_utils.parse_comment(field['comment'])
    if isinstance(sqlalchemy_type, TINYINT):
        if not field_mappping:
            return '布尔框'

    return comp_name


def get_field_label(field):
    # 获取字段标签
    comment = field['comment'] or field['name']
    field_label, _ = db_utils.parse_comment(comment)
    if not field_label:
        field_label = field['name']
    return field_label

###################### 字段处理 END ######################
