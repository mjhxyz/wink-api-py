from wink.api.base import api
from wink.models.field import WinkField
from wink.models.mapping import WinkMapping
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.api.views.menu import WinkMenuView
from wink.common import db_utils

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
        meta_code=data['meta_code'],
        weight=data['weight'],
        name=data['name'],
        label=data['label'],
        type=data['type'],
        exp=data['exp'],
        width=data['width'],
        align=data['align'],
        placeholder=data['placeholder'],
        required=data['required'],
        is_hide=data['is_hide'],
        max_length=data['max_length'],
        min_length=data['min_length'],
        default_value=data['default_value'],
        is_editable=data['is_editable'],
        is_addable=data['is_addable'],
        # is_edit=data['is_edit'],
        # is_add=data['is_add'],
        # add_status=data['add_status'],
        # edit_status=data['edit_status'],
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
    field.meta_code = data['meta_code']
    field.weight = data['weight']
    field.name = data['name']
    field.label = data['label']
    field.type = data['type']
    field.exp = data['exp']
    field.width = data['width']
    field.align = data['align']
    field.placeholder = data['placeholder']
    field.required = data['required']
    field.is_hide = data['is_hide']
    field.max_length = data['max_length']
    field.min_length = data['min_length']
    field.default_value = data['default_value']
    field.is_edit = data['is_edit']
    field.is_add = data['is_add']
    # field.add_status = data['add_status']
    # field.edit_status = data['edit_status']
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


@api.get('/field/mapping')
@login_required
def field_mapping():
    args = request.args
    field_id = args.get('field_id')
    if not field_id:
        raise NotFoundError('获取映射失败,没有提供 field_id')
    # TODO 表单验证
    field = WinkField.query.filter_by(id=field_id).first()
    if not field:
        raise NotFoundError('字段不存在')
    if field.compo != '下拉框':
        raise NotFoundError('字段组件类型不是下拉框')
    exp = field.exp
    if not exp:
        return Success([])
    if exp.index(';') == -1:
        raise NotFoundError('字段映射表达式错误')
    exp_list = exp.split(';')
    if len(exp_list) != 2:
        raise NotFoundError('字段映射表达式错误')
    sql, source = exp_list
    print(sql, source)
    result = db_utils.execute_sql(source, sql)
    return Success(result)
