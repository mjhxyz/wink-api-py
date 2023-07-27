# 查找框接口
from wink.api.base import api
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.models.meta import WinkMeta
from wink.models.field import WinkField
from wink.common import db_utils

from sqlalchemy import inspect, select
from flask import current_app, request
from sqlalchemy.exc import NoSuchTableError
from flask_login import login_required


@api.get('/wink/widget/find')
def wink_widget_find():
    args = request.args
    # TODO 表单验证
    meta_code = args.get('meta_code')
    field_name = args.get('field_name')
    # 通过 meta_code 和 field_name 查找字段
    field = WinkField.query.filter_by(
        meta_code=meta_code, name=field_name).first()
    if not field:
        return NotFoundError('字段不存在')
    exp = field.exp
    if not exp:
        return NotFoundError('字段没有表达式')
    sql, source = db_utils.get_source_str(exp)
    res, field_list = db_utils.query_sql(source, sql)
    return Success({
        'data': res,
        'field_list': field_list,
    })
