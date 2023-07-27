from wink.models.base import db
from wink.common.resp import NotFoundError

from sqlalchemy import inspect, MetaData, Table
from flask import current_app
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import Integer, String, Text, Float, Date, DateTime, Boolean, JSON, LargeBinary, Numeric
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import text


def get_source_str(exp):
    if not exp:
        raise NotFoundError('表达式格式错误')
    exp = exp.strip()
    if not exp:
        raise NotFoundError('表达式格式错误')
    exp_list = exp.split(';')
    if len(exp_list) != 2:
        raise NotFoundError('表达式格式错误')
    return exp_list


def get_source_engine(source):
    config = current_app.config
    if source == 'meta':
        return db.engine
    if not is_source_exists(source):
        raise NotFoundError('数据源不存在')
    db_bi = config['DB_BI']
    return db.get_engine(source)


def query_sql(source, sql):
    engine = get_source_engine(source)
    with engine.connect() as conn:
        if isinstance(sql, str):
            sql = text(sql)
        res = conn.execute(sql)
        field_list = res.keys()
        mapping_list = res.mappings().all()
        result = []
        for mapping in mapping_list:
            result.append(dict(mapping))
        return result, list(field_list)
    


def execute_sql(source, sql):
    engine = get_source_engine(source)
    with engine.connect() as conn:
        if isinstance(sql, str):
            sql = text(sql)
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


def get_field_label(field):
    # 获取字段标签
    comment = field['comment'] or field['name']
    field_label, _ = parse_comment(comment)
    return field_label

###################### 字段处理 END ######################


def save_table_record(source, table, data):
    # 保存数据
    engine = get_source_engine(source)
    table = generate_table(source, table)
    with engine.connect() as conn:
        conn.execute(table.insert(), data)
        conn.commit()
    return data


def edit_table_record(source, table, pk, pk_val, data):
    # 更新数据
    engine = get_source_engine(source)
    table = generate_table(source, table)
    with engine.connect() as conn:
        conn.execute(table.update().where(
            getattr(table.c, pk) == pk_val), data)
        conn.commit()
    return data


def edit_delete_one_record(source, table, pk, pk_val):
    # 删除数据
    engine = get_source_engine(source)
    table = generate_table(source, table)
    with engine.connect() as conn:
        conn.execute(table.delete().where(
            getattr(table.c, pk) == pk_val))
        conn.commit()


def edit_delete_many_record(source, table, pk, pk_val_list):
    # 批量删除数据
    engine = get_source_engine(source)
    table = generate_table(source, table)
    with engine.connect() as conn:
        conn.execute(table.delete().where(
            getattr(table.c, pk).in_(pk_val_list)))
        conn.commit()
