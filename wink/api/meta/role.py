from wink.api.base import api
from wink.models.role import WinkRole
from wink.models.base import db
from wink.common.resp import Success, NotFoundError, List

from flask import request, jsonify


@api.get('/role/list')
def role_list():
    roles = WinkRole.query.all()
    return List(len(roles), roles, 1)


@api.post('/role/add')
def role_add():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    role = WinkRole(
        name=data['name'],
        desc=data['desc'],
    )
    db.session.add(role)
    db.session.commit()

    return Success()


@api.post('/role/edit')
def role_edit():
    # 获取 json 数据
    data = request.get_json()
    # TODO 表单验证
    role = WinkRole.query.filter_by(id=data['id']).first()
    if not role:
        return NotFoundError('角色不存在')
    role.name = data['name']
    role.desc = data['desc']
    db.session.commit()
    return Success()
