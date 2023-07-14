from wink.api.base import api
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.common import db_utils

from sqlalchemy import inspect
from flask import current_app, request
from sqlalchemy.exc import NoSuchTableError
from flask_login import login_required


# 一定要鉴权
@api.get('/wink/db/table_list')
@login_required
def db_table_list():
    source = request.args.get('source', 'meta')
    table_names = db_utils.get_table_list(source)
    return Success(data=table_names)


# 一定要鉴权
@api.get('/wink/db/source_list')
@login_required
def db_source_list():
    result = db_utils.get_source_list()
    return Success(data=result)


# 一定要鉴权
@api.get('/wink/db/table_field_list')
@login_required
def table_field_list():
    table_name = request.args.get('table_name')
    source = request.args.get('source', 'meta')
    result = db_utils.get_table_field_list(source, table_name)
    return Success(data=result)
