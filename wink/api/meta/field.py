from wink.api.base import api
from wink.models.field import WinkField
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.api.views.menu import WinkMenuView

from flask import request
from flask_login import current_user, login_required


@api.get('/field/list')
@login_required
def field_list():
    query = WinkField.query
    # query 中只使用 masterKey 的作为查询条件
    if 'masterKey' in request.args:
        query = query.filter_by(meta_code=request.args['masterKey'])
    fields = query.all()
    return List(len(fields), fields, 1)


@api.post('/field/add')
@login_required
def field_add():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    field = WinkField.query.filter_by(name=data['name']).first()
    if field:
        return NotFoundError('字段已存在')
    field = WinkField(
        code=data['code'],
        name=data['name'],
        type=data['type'],
        weight=data['weight'],
        parent_id=data['parent_id'],
        setting=data['setting'],
    )

    db.session.add(field)
    db.session.commit()
    return Success()


@api.post('/field/edit')
@login_required
def field_edit():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    field = WinkField.query.filter_by(id=data['id']).first()
    if not field:
        return NotFoundError('field 不存在')
    field.code = data['code']
    field.name = data['name']
    field.type = data['type']
    field.weight = data['weight']
    field.parent_id = data['parent_id']
    field.setting = data['setting']
    db.session.commit()
    return Success()


@api.post('/field/delete')
@login_required
def field_delete():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    field = WinkField.query.filter_by(id=data['id']).first()
    if not field:
        return NotFoundError('field 不存在')
    db.session.delete(field)
    db.session.commit()
    return Success()


@api.post('/field/delete_many')
@login_required
def field_delete_many():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    fields = WinkField.query.filter(WinkField.id.in_(data['ids'])).all()
    if not fields:
        return NotFoundError('field 不存在')
    for field in fields:
        db.session.delete(field)
    db.session.commit()
    return Success()
