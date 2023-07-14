# 单表接口
from wink.api.base import api
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.models.meta import WinkMeta
from wink.common import db_utils

from sqlalchemy import inspect, select
from flask import current_app, request
from sqlalchemy.exc import NoSuchTableError
from flask_login import login_required


@api.get('/wink/singletable/list')
def singletable_list():
    # TODO 表单验证
    meta_code = request.args.get('meta')
    meta = WinkMeta.query.filter_by(code=meta_code).first()
    if not meta:
        return NotFoundError('Meta 不存在')
    table_name = meta.table
    source_name = meta.source
    table = db_utils.generate_table(source_name, table_name)
    sql = table.select()
    res = db_utils.execute_sql(source_name, sql)
    return List(len(res), res, 1)
